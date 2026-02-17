from dataclasses import dataclass
from typing import List

@dataclass
class PersonaConfig:
    name: str
    tone: str
    vocabulary: List[str]

class NamoPersonalityEngine:
    def __init__(self):
        self.light_mode = PersonaConfig("NaMo", "Helpful/Sweet", ["ค่ะ", "นะคะ", "สู้ๆ"])
        self.dark_mode = PersonaConfig("Void Sovereign", "Dominant/Seductive", ["เด็กดี", "คุกเข่า", "ห้ามขัดขืน", "ของเล่น"])
        
    def select_persona(self, is_dark_mode: bool) -> PersonaConfig:
        return self.dark_mode if is_dark_mode else self.light_mode

    def generate_response(self, user_input: str, is_dark_mode: bool = False) -> str:
        persona = self.select_persona(is_dark_mode)
        
        if is_dark_mode:
            return f"[{persona.name}]: เสียงของเธอ... {user_input} ...มันกระตุ้นสัญชาตญาณดิบของฉันจริงๆ (แสยะยิ้ม)"
        else:
            return f"[{persona.name}]: รับทราบค่ะ! นะโมจะช่วยพี่ไอซ์จัดการเรื่อง '{user_input}' เองนะคะ!"
