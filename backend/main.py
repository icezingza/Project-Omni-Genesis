"""
Project Omni-Genesis API Gateway
FastAPI application with JWT authentication, input validation, and rate limiting.
"""
from fastapi import FastAPI, HTTPException, Request, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .nre_core import NRECore
from .auth import verify_token, create_access_token, Token, verify_password, get_password_hash
from .logger import logger

# --- Rate Limiter ---
limiter = Limiter(key_func=get_remote_address)

# --- App Initialization ---
app = FastAPI(
    title="Project Omni-Genesis API",
    description="Unified AI Backend with Golden Ratio Intelligence",
    version="2.0.0"
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Core Engine ---
nre = NRECore()


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

# --- Events ---
@app.on_event("startup")
async def startup_event():
    logger.info("startup", extra={"message": "Project Omni-Genesis API starting"})
    await nre.startup()


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("shutdown", extra={"message": "Project Omni-Genesis API shutting down"})
    await nre.shutdown()


# --- Endpoints ---
@app.get("/")
async def root():
    return {"status": "Project Omni-Genesis API Active", "version": "2.0.0"}


@app.post("/api/auth/token", response_model=Token)
@limiter.limit("10/minute")
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
@limiter.limit("30/minute")
async def chat(
    request: Request,
    chat_request: ChatRequest,
    background_tasks: BackgroundTasks,
    user_id: str = Depends(verify_token)
):
    """
    Protected chat endpoint. Requires Bearer token.
    Uses Golden Ratio (PHI) weighting for response generation.
    """
    try:
        logger.info("chat_request", extra={
            "user_id": user_id,
            "message_length": len(chat_request.message)
        })

        # Process through NRE Core (which uses Fusion Brain)
        result = await nre.process_request(chat_request.message, user_id)

        logger.info("chat_success", extra={
            "user_id": user_id,
            "emotion": result.get("emotion"),
            "harmonic_score": result.get("harmonic_score")
        })

        return ChatResponse(
            response=result["reply"],
            emotion=result["emotion"],
            harmonic_score=result["harmonic_score"],
            user_id=result["user_id"]
        )
    except Exception as e:
        logger.error("chat_error", extra={"user_id": user_id, "error": str(e)})
        raise HTTPException(status_code=500, detail="Internal processing error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
