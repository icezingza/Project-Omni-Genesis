import json
import os
from dotenv import load_dotenv

# Import Modules
from nre_core import NRECore
from core.fusion_brain import FusionBrain
from core.rag_memory_system import RAGMemorySystem

# Load Config
load_dotenv()
try:
    with open("config.json", "r", encoding="utf-8") as f:
        CONFIG = json.load(f)
except FileNotFoundError:
    CONFIG = {"bot_name": "Namo", "memory_path": "./data"}

def main():
    # 1. Initialize Body (เริ่มระบบพื้นฐาน)
    nre = NRECore()
    nre.boot_system()

    # 2. Initialize Memory (โหลดความจำ)
    memory = RAGMemorySystem(CONFIG)

    # 3. Initialize Brain (ปลุกสมอง)
    brain = FusionBrain(CONFIG)

    print("\n✨ NamoNexus is ready! (Type 'exit' to quit)\n")

    # 4. Main Loop (วงจรชีวิตหลัก)
    while True:
        try:
            user_input = input("👤 P'Ice: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("👋 Namo: ไว้เจอกันใหม่นะคะพี่ไอซ์")
                break

            # --- Step A: Retrieve Context (ดึงข้อมูลเก่า) ---
            related_memories = memory.retrieve(user_input)

            # --- Step B: Think & Feel (ประมวลผล + ความรู้สึก) ---
            # ส่ง input และ memory ไปให้สมองคิด
            thought_process = brain.process_thought(user_input, related_memories)
            final_response = thought_process["response"]

            # --- Step C: Respond (ตอบโต้) ---
            print(f"🤖 Namo: {final_response}")
            # (Optional Debug info)
            # print(f"   [Debug] Sentiment: {thought_process['sentiment_detected']}")

            # --- Step D: Learn (บันทึกข้อมูลใหม่) ---
            memory.save_interaction(user_input, final_response)
            
            # --- Step E: System Check (ตรวจสอบสุขภาพระบบ) ---
            health = nre.check_health()
            if health['cpu'] > 80:
                print("⚠️ [Warning] CPU Usage High!")

        except KeyboardInterrupt:
            break
        except Exception as e:
            nre.log_activity("ERROR", str(e))
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
