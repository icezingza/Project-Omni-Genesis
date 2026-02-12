"""
Project Omni-Genesis API Gateway
FastAPI application with JWT authentication, input validation, rate limiting,
Golden Ratio emotion analysis, and NaMo personality engine.
"""
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, Depends, BackgroundTasks, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .nre_core import NRECore
from .auth import verify_token, create_access_token, Token, verify_password, get_password_hash
from .services.golden_ratio_emotion import GoldenRatioEmotionAnalyzer
from .logger import logger
from .config import settings
from .services.emotion_detector import EmotionDetector
from .services.namo_personality import NaMoPersonality
from .analytics import router as analytics_router, _record_interaction

# --- Rate Limiter ---
limiter = Limiter(key_func=get_remote_address)

# --- Core Engine ---
nre = NRECore()
emotion_analyzer = GoldenRatioEmotionAnalyzer()

# --- AI Services ---
emotion_detector = EmotionDetector()
namo = NaMoPersonality()


# --- Lifespan (replaces deprecated on_event) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle management."""
    logger.info("startup", extra={"message": f"{settings.APP_NAME} API starting v{settings.APP_VERSION}"})
    await nre.startup()
    yield
    logger.info("shutdown", extra={"message": f"{settings.APP_NAME} API shutting down"})
    await nre.shutdown()


# --- App Initialization ---
app = FastAPI(
    title=settings.APP_NAME,
    description="Unified AI Backend with Golden Ratio Intelligence",
    version=settings.APP_VERSION,
    lifespan=lifespan,
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Exception Handlers ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "message": "Validation error. Please check your input."
        }
    )


# --- Include Routers ---
app.include_router(analytics_router)


# --- Models with Validation ---
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    voice_features: Optional[Dict] = None
    facial_features: Optional[Dict] = None

    @field_validator('message')
    @classmethod
    def sanitize_message(cls, v: str) -> str:
        """Strip whitespace and basic sanitization."""
        return v.strip()


class ChatResponse(BaseModel):
    response: str
    emotion: str
    harmonic_score: float
    user_id: str
    namo_mood: Optional[str] = None
    balance_index: Optional[float] = None


class EmotionAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    has_history: bool = False


class EmotionAnalysisResponse(BaseModel):
    emotion: float
    logic: float
    combined: float
    confidence: float
    strategy: str


class LoginRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=4, max_length=100)

    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls, v: str) -> str:
        """Ensure user_id is alphanumeric."""
        clean = v.strip()
        if not clean.replace("-", "").replace("_", "").isalnum():
            raise ValueError('user_id must be alphanumeric (with optional - or _)')
        return clean

# --- Mock User Database (Replace with real DB in production) ---
# Default admin password is "admin123"
FAKE_USERS_DB = {
    "admin": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
    "namo_dev": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
}



# --- Endpoints ---
@app.get("/")
async def root():
    return {"status": f"{settings.APP_NAME} API Active", "version": settings.APP_VERSION}


@app.get("/api/health")
async def health_check():
    """System health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "services": {
            "nre_core": nre.status,
            "emotion_detector": "active",
            "namo_personality": namo.mood,
        },
        "namo_state": namo.get_state(),
    }


@app.post("/api/auth/token", response_model=Token)
@limiter.limit(f"{settings.AUTH_RATE_LIMIT_PER_MINUTE}/minute")
async def login_for_token(request: Request, login: LoginRequest):
    """Generate an access token for a user."""
    logger.info("token_request", extra={"user_id": login.user_id})
    
    # Verify user (Mock implementation)
    user_hash = FAKE_USERS_DB.get(login.user_id)
    if not user_hash or not verify_password(login.password, user_hash):
        logger.warning("login_failed", extra={"user_id": login.user_id})
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user_id=login.user_id)
    return Token(access_token=access_token, token_type="bearer")


@app.post("/api/chat", response_model=ChatResponse)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def chat(
    request: Request,
    chat_request: ChatRequest,
    background_tasks: BackgroundTasks,
    user_id: str = Depends(verify_token)
):
    """
    Protected chat endpoint. Requires Bearer token.
    Uses Golden Ratio (PHI) weighting for response generation.
    Integrates EmotionDetector and NaMo personality.
    """
    try:
        logger.info("chat_request", extra={
            "user_id": user_id,
            "message_length": len(chat_request.message)
        })

        # Step 1: Detect emotion using Thai NLP + Golden Ratio
        emotion_result = emotion_detector.detect(chat_request.message)

        # Step 2: Process through NRE Core (which uses Fusion Brain)
        result = await nre.process_request(chat_request.message, user_id)

        # Step 3: Generate NaMo personality response
        personality_response = namo.generate_response(
            user_message=chat_request.message,
            emotion=emotion_result.emotion,
            formality=emotion_result.formality,
        )

        # Use NaMo's response if Fusion Brain gives a generic one
        final_reply = result.get("reply", personality_response.message)
        final_emotion = emotion_result.emotion
        final_harmonic = emotion_result.harmonic_score

        # Step 4: Record interaction for analytics (background)
        background_tasks.add_task(
            _record_interaction,
            user_id,
            final_emotion,
            final_harmonic,
        )

        logger.info("chat_success", extra={
            "user_id": user_id,
            "emotion": final_emotion,
            "harmonic_score": final_harmonic,
            "namo_mood": namo.mood,
        })

        return ChatResponse(
            response=final_reply,
            emotion=final_emotion,
            harmonic_score=final_harmonic,
            user_id=user_id,
            namo_mood=namo.mood,
            balance_index=emotion_result.balance_index,
        )
    except Exception as e:
        logger.error("chat_error", extra={"user_id": user_id, "error": str(e)})
        raise HTTPException(status_code=500, detail="Internal processing error")


@app.post("/api/emotion/analyze", response_model=EmotionAnalysisResponse)
@limiter.limit("60/minute")
async def analyze_emotion(request: Request, payload: EmotionAnalysisRequest):
    """Analyze text emotion/logic with Golden Ratio weighted scoring."""
    analysis = emotion_analyzer.analyze(
        payload.text,
        context={"has_history": payload.has_history},
    )
    return EmotionAnalysisResponse(**analysis)


@app.get("/api/namo/greeting")
async def namo_greeting(user_id: str = Depends(verify_token)):
    """Get NaMo's current greeting based on her mood."""
    return {
        "greeting": namo.get_greeting(),
        "mood": namo.mood,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
