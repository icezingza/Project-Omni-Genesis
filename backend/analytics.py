"""
Project Omni-Genesis: Analytics API Router
Provides endpoints for user dashboard data and emotion trend analysis.
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, Query

from .auth import verify_token

logger = logging.getLogger("omni_genesis.analytics")

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


# --- In-memory analytics store (production would use database) ---
_analytics_store: Dict[str, List[Dict]] = {}


def _record_interaction(user_id: str, emotion: str, harmonic_score: float) -> None:
    """Record an interaction for analytics (called from chat endpoint)."""
    if user_id not in _analytics_store:
        _analytics_store[user_id] = []

    _analytics_store[user_id].append({
        "emotion": emotion,
        "harmonic_score": harmonic_score,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


@router.get("/dashboard")
async def get_dashboard(user_id: str = Depends(verify_token)):
    """
    Get user analytics dashboard summary.

    Returns total interactions, common emotions, average harmonic score.
    """
    interactions = _analytics_store.get(user_id, [])

    if not interactions:
        return {
            "user_id": user_id,
            "total_interactions": 0,
            "top_emotions": [],
            "avg_harmonic_score": 0.0,
            "message": "No interactions recorded yet.",
        }

    # Count emotions
    emotion_counts: Dict[str, int] = {}
    total_harmonic = 0.0

    for interaction in interactions:
        emotion = interaction["emotion"]
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        total_harmonic += interaction["harmonic_score"]

    # Sort emotions by frequency
    top_emotions = sorted(
        emotion_counts.items(),
        key=lambda x: x[1],
        reverse=True,
    )[:5]

    avg_harmonic = total_harmonic / len(interactions) if interactions else 0.0

    return {
        "user_id": user_id,
        "total_interactions": len(interactions),
        "top_emotions": [{"emotion": e, "count": c} for e, c in top_emotions],
        "avg_harmonic_score": round(avg_harmonic, 4),
    }


@router.get("/emotions")
async def get_emotion_trends(
    user_id: str = Depends(verify_token),
    days: int = Query(default=7, ge=1, le=90, description="Number of days to look back"),
):
    """
    Get emotion trends over time for the authenticated user.

    Args:
        days: Number of days to look back (1-90, default 7).
    """
    interactions = _analytics_store.get(user_id, [])
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    # Filter by date range
    recent = []
    for interaction in interactions:
        try:
            ts = datetime.fromisoformat(interaction["timestamp"])
            if ts >= cutoff:
                recent.append(interaction)
        except (ValueError, KeyError):
            continue

    if not recent:
        return {
            "user_id": user_id,
            "period_days": days,
            "trends": [],
            "message": f"No interactions in the last {days} days.",
        }

    # Group by date
    daily: Dict[str, Dict[str, int]] = {}
    for interaction in recent:
        date_key = interaction["timestamp"][:10]  # YYYY-MM-DD
        if date_key not in daily:
            daily[date_key] = {}
        emotion = interaction["emotion"]
        daily[date_key][emotion] = daily[date_key].get(emotion, 0) + 1

    trends = [
        {"date": date, "emotions": emotions}
        for date, emotions in sorted(daily.items())
    ]

    return {
        "user_id": user_id,
        "period_days": days,
        "trends": trends,
    }
