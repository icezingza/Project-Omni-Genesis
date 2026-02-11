"""PDPA compliance helpers for handling personal data safely."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


class PDPACompliance:
    """Utility methods for common PDPA operations."""

    REDACT_FIELDS = {
        "full_name",
        "first_name",
        "last_name",
        "phone",
        "phone_number",
        "email",
        "line_id",
        "address",
    }

    @classmethod
    def anonymize_conversation(cls, conversation: dict[str, Any]) -> dict[str, Any]:
        """Return a copy of conversation payload with common PII fields redacted."""
        payload = deepcopy(conversation)

        def scrub(node: Any) -> Any:
            if isinstance(node, dict):
                return {
                    key: ("[REDACTED]" if key in cls.REDACT_FIELDS else scrub(value))
                    for key, value in node.items()
                }
            if isinstance(node, list):
                return [scrub(item) for item in node]
            return node

        return scrub(payload)

    @staticmethod
    def get_user_data_export(user_id: str, profile: dict[str, Any], conversations: list[dict[str, Any]]) -> dict[str, Any]:
        """Create a structured payload for data portability requests."""
        return {
            "user_id": user_id,
            "profile": deepcopy(profile),
            "conversations": deepcopy(conversations),
            "export_format": "json",
            "compliance": "PDPA-data-portability",
        }

    @staticmethod
    def delete_user_data(user_id: str, store: dict[str, Any]) -> bool:
        """Delete user data from an in-memory store-like object."""
        existed = user_id in store
        store.pop(user_id, None)
        return existed
