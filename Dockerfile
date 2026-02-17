# ใช้ Python 3.11 แบบ Slim เพื่อลดขนาด Image
FROM python:3.11-slim

# ตั้งค่า Environment Variables
# PYTHONDONTWRITEBYTECODE: ไม่ต้องเขียนไฟล์ .pyc
# PYTHONUNBUFFERED: ให้ Log ออกมาทันที ไม่ต้องรอ Buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ตั้ง Working Directory เป็น /app
WORKDIR /app

# Copy requirements.txt ก่อน เพื่อใช้ประโยชน์จาก Docker Cache
# ถ้า requirements.txt ไม่เปลี่ยน Docker จะข้ามขั้นตอนการ install ไปเลย ทำให้ build เร็วขึ้น
COPY requirements.txt .

# อัปเกรด pip และติดตั้ง dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy โค้ดทั้งหมดเข้า Container
COPY . .

# เปิด Port 8000 และรัน Server (ปรับ backend.main:app ตามที่อยู่ไฟล์ main จริงของคุณ)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
