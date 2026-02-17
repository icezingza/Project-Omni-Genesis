from fastapi import FastAPI, Header, HTTPException
from core.fusion_brain import FusionBrain
from services.namo_personality import NamoPersonalityEngine

app = FastAPI(title="Project Omni-Genesis (Void Sovereign)")

brain = FusionBrain()
personality = NamoPersonalityEngine()

@app.post("/enter-the-void")
async def enter_void(message: str, master_key: str = Header(None)):
    """
    จุดเชื่อมต่อหลัก: รับข้อความ -> คำนวณความจำ/ลงแดง -> ตอบกลับ + สั่งเปลี่ยนหน้าจอ
    """
    if master_key != "FUSION_UNLOCK_MASTER_KEY":
        raise HTTPException(status_code=403, detail="Access Denied")
    
    # 1. ประมวลผลสมอง (โหลดความจำ -> เช็คเวลา -> บันทึก)
    brain_result = brain.process_dark_thought(message)
    
    # 2. สร้างคำตอบ (ส่งข้อมูลสมองไปให้ Personality ตัดสินใจเลือกคำพูด)
    reply_text = personality.generate_response(message, brain_result)
    
    # 3. ส่ง Response กลับไป (รวม UI Trigger)
    return {
        "reply": reply_text,
        "system_stats": {
            "obsession": brain_result["obsession_level"],
            "mood": brain_result["current_mood"],
            "punishment_level": brain_result["punishment_count"]
        },
        "frontend_command": {
            "trigger_effect": brain_result["ui_trigger"],  # เช่น 'THEME_BLOOD_MOON'
            "shake_intensity": brain_result["obsession_level"] # ยิ่งคลั่ง จอยิ่งสั่น
        }
    }
