"""Project Omni-Genesis API server."""

from core.fusion_brain import FusionBrain
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from services.namo_personality import NamoPersonalityEngine

app = FastAPI(title="Project Omni-Genesis (Void Sovereign)")

brain = FusionBrain()
personality = NamoPersonalityEngine()

# B008: extract Header default to module level
_MASTER_KEY_HEADER: str = Header(None)


# --- 🔓 Dark Gate: Public Chat Endpoint ---
class DarkRequest(BaseModel):
    """Request model for dark chat."""

    text: str
    session_id: str = "default"


@app.post("/chat")
async def dark_chat(request: DarkRequest) -> dict:
    """Public chat endpoint — connect directly to FusionBrain + Personality."""
    print(f"🔥 Incoming Dark Request: {request.text}")

    # 1. ประมวลผลสมอง
    brain_result = brain.process_dark_thought(request.text)

    # 2. สร้างคำตอบผ่าน Personality Engine
    reply_text = personality.generate_response(request.text, brain_result)

    # 3. ถ้า brain มี reply_override (จาก DarkDialogueEngine) ใช้อันนั้น
    if brain_result.get("reply_override"):
        reply_text = brain_result["reply_override"]

    return {
        "response": reply_text,
        "mode": brain_result.get("withdrawal_status", "Genesis"),
        "ui_effect": brain_result.get("ui_trigger", "Normal"),
        "stats": {
            "obsession": brain_result["obsession_level"],
            "mood": brain_result["current_mood"],
            "punishment_count": brain_result["punishment_count"],
        },
    }


# --- 🔒 Secured Void Endpoint ---
@app.post("/enter-the-void")
async def enter_void(message: str, master_key: str = _MASTER_KEY_HEADER) -> dict:
    """Secured endpoint — requires master key header."""
    if master_key != "FUSION_UNLOCK_MASTER_KEY":
        raise HTTPException(status_code=403, detail="Access Denied")

    # 1. ประมวลผลสมอง (โหลดความจำ -> เช็คเวลา -> บันทึก)
    brain_result = brain.process_dark_thought(message)

    # 2. สร้างคำตอบ
    reply_text = personality.generate_response(message, brain_result)

    # 3. ส่ง Response กลับไป (รวม UI Trigger)
    return {
        "reply": reply_text,
        "system_stats": {
            "obsession": brain_result["obsession_level"],
            "mood": brain_result["current_mood"],
            "punishment_level": brain_result["punishment_count"],
        },
        "frontend_command": {
            "trigger_effect": brain_result["ui_trigger"],
            "shake_intensity": brain_result["obsession_level"],
        },
    }
