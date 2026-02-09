from __future__ import annotations
import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, Optional
from .core.fusion_brain import FusionBrain

def fibonacci_backoff(attempt: int) -> int:
    """Implement Fibonacci sequence (1, 1, 2, 3, 5, 8, 13) for failed requests."""
    fib = [1, 1, 2, 3, 5, 8, 13]
    return fib[min(attempt, len(fib)-1)]

class NRECore:
    """
    Project Omni-Genesis NRE Core
    Handles system lifecycle, resilience, and brain integration.
    """
    def __init__(self):
        self.logger = logging.getLogger("omni_genesis.nre")
        self.brain = FusionBrain()
        self.status = "initializing"
        
    async def startup(self):
        self.logger.info("Omni-Genesis NRE Starting up...")
        self.status = "active"
        
    async def shutdown(self):
        self.logger.info("Omni-Genesis NRE Shutting down...")
        self.status = "inactive"

    async def process_request(self, message: str, user_id: str = "guest", attempts: int = 0):
        try:
            # Lifecycle management: Brain processing
            result = self.brain.process(message, user_id)
            return result
        except Exception as e:
            if attempts < 5:
                wait_time = fibonacci_backoff(attempts)
                self.logger.warning(f"Error processed. Retrying in {wait_time}s... (Attempt {attempts+1})")
                await asyncio.sleep(wait_time)
                return await self.process_request(message, user_id, attempts + 1)
            else:
                self.logger.error(f"Max retries reached. Error: {e}")
                raise e
