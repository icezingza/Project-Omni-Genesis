"""
Project Omni-Genesis: Structured JSON Logging Module
Provides anonymized, production-ready logging for PDPA compliance.
"""
import logging
import sys
import hashlib
from datetime import datetime
from typing import Any, Dict

from pythonjsonlogger import jsonlogger


class AnonymizedFormatter(jsonlogger.JsonFormatter):
    """
    Custom JSON formatter that anonymizes user-identifying data for PDPA compliance.
    """
    SENSITIVE_FIELDS = ["user_id", "ip_address", "email"]

    def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]):
        super().add_fields(log_record, record, message_dict)
        log_record["timestamp"] = datetime.utcnow().isoformat() + "Z"
        log_record["level"] = record.levelname
        log_record["service"] = "omni-genesis"

        # Anonymize sensitive fields
        for field in self.SENSITIVE_FIELDS:
            if field in log_record and log_record[field]:
                log_record[field] = self._anonymize(str(log_record[field]))

    def _anonymize(self, value: str) -> str:
        """Hash the value to anonymize it while maintaining consistency."""
        return hashlib.sha256(value.encode()).hexdigest()[:16]


def get_logger(name: str = "omni_genesis") -> logging.Logger:
    """
    Get a configured logger instance with JSON formatting.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = AnonymizedFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


# Default logger instance
logger = get_logger()
