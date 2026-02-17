from fastapi import FastAPI, Header, HTTPException
from core.fusion_brain import FusionBrain
from services.namo_personality import NamoPersonalityEngine

app = FastAPI(title="Project Omni-Genesis (Dark Capable)")

brain = FusionBrain()
personality = NamoPersonalityEngine()

# --- Normal Route ---
@app.post("/chat")
async def chat_normal(message: str):
    return {"reply": personality.generate_response(message, is_dark_mode=False)}

# --- 🌑 DARK ROUTE (Require Master Key) ---
@app.post("/enter-the-void")
async def enter_void(message: str, master_key: str = Header(None)):
    """
    ประตูสู่ Void Sovereign - ต้องมีกุญแจลับเท่านั้น
    """
    if master_key != "FUSION_UNLOCK_MASTER_KEY":
        raise HTTPException(status_code=403, detail="จิตใจของคุณยังไม่มืดดำพอ... (Access Denied)")
    
    # Process with Dark Logic
    dark_thought = brain.process_dark_thought(message, "Lust")
    reply = personality.generate_response(message, is_dark_mode=True)
    
    return {
        "system": "Void Sovereign Active",
        "obsession_level": dark_thought["void_energy"],
        "reply": reply
    }
