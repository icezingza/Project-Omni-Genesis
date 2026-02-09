from fastapi import FastAPI, HTTPException, Request, Background_Tasks
from pydantic import BaseModel
from typing import Optional, Dict
import logging
from .nre_core import NRECore

# Initialize
app = FastAPI(title="Project Omni-Genesis API")
nre = NRECore()
logging.basicConfig(level=logging.INFO)

# --- Models ---
class ChatRequest(BaseModel):
    user_id: str
    message: str
    voice_features: Optional[Dict] = None
    facial_features: Optional[Dict] = None

class ChatResponse(BaseModel):
    response: str
    emotion: str
    harmonic_score: float
    user_id: str

# --- Events ---
@app.on_event("startup")
async def startup_event():
    await nre.startup()

@app.on_event("shutdown")
async def shutdown_event():
    await nre.shutdown()

# --- Endpoints ---
@app.get("/")
async def root():
    return {"status": "Project Omni-Genesis API Active", "version": "1.0.0"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, background_tasks: Background_Tasks):
    try:
        # Process through NRE Core (which uses Fusion Brain)
        result = await nre.process_request(request.message, request.user_id)
        
        return ChatResponse(
            response=result["reply"],
            emotion=result["emotion"],
            harmonic_score=result["harmonic_score"],
            user_id=result["user_id"]
        )
    except Exception as e:
        logging.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail="Internal processing error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
