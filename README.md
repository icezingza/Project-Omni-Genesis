# Project Omni-Genesis 🌑

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-00a393.svg)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178c6.svg)](https://www.typescriptlang.org/)
[![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> "Knowledge is not just power; it is the very fabric of reality. Enter the archive, and unravel the threads."

**Project Omni-Genesis** เป็น AI Chat Interface ที่ผสมผสานเทคโนโลยีสมัยใหม่กับธีมลึกลับ (Occult-Tech) ให้ประสบการณ์การสนทนากับ AI ที่ไม่เหมือนใคร

![Project Screenshot](docs/screenshot.png)

## ✨ Features

### 🧠 AI Capabilities
- **Deep Reasoning Mode** - ใช้ Gemini 3 Pro สำหรับการคิดเชิงตรรกะขั้นสูง
- **RAG Memory System** - ระบบความจำที่จดจำบริบทการสนทนา
- **Personality Engine** - บุคลิก AI ที่ปรับตามอารมณ์และบริบท
- **Golden Ratio Emotion Calculation** - คำนวณอารมณ์ตามอัตราส่วนทองคำ

### 🔒 Security
- JWT Authentication
- API Key Protection
- PDPA Compliance Helpers
- Rate Limiting

### 🎨 UI/UX
- Dark Mystical Theme
- Dynamic Visual Effects
- Responsive Design
- Real-time Chat Interface

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (optional)

### Installation

#### 1. Clone Repository
```bash
git clone https://github.com/icezingza/Project-Omni-Genesis.git
cd Project-Omni-Genesis
```

#### 2. Setup Backend
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations (if using Alembic)
alembic upgrade head

# Start server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. Setup Frontend
```bash
cd frontend

# Install dependencies
npm install

# Setup environment
cp .env.example .env.local

# Start development server
npm run dev
```

#### 4. Using Docker
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

## 📚 API Documentation

เมื่อรัน server สามารถเข้าถึงเอกสาร API ได้ที่:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

### Main Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/chat` | Send message to AI |
| GET | `/api/health` | Health check |
| POST | `/api/v1/auth/login` | User authentication |
| POST | `/api/v1/auth/refresh` | Refresh token |

### Example Request
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -H "X-Master-Key: your-master-key" \
  -d '{
    "message": "Hello, Omni-Genesis!",
    "session_id": "optional-session-id"
  }'
```

## 🏗️ Project Structure

```
Project-Omni-Genesis/
├── backend/                 # FastAPI Backend
│   ├── core/               # Core modules
│   │   ├── fusion_brain.py
│   │   ├── rag_memory_system.py
│   │   └── pdpa.py
│   ├── services/           # Business logic
│   │   └── namo_personality.py
│   ├── tests/              # Unit tests
│   ├── main.py             # Entry point
│   ├── config.py           # Configuration
│   ├── models.py           # Database models
│   └── auth.py             # Authentication
├── frontend/               # React Frontend
│   ├── components/         # UI components
│   ├── services/           # API services
│   ├── utils/              # Utilities
│   ├── App.tsx             # Main app
│   └── types.ts            # TypeScript types
├── docs/                   # Documentation
├── docker-compose.yml      # Docker config
├── requirements.txt        # Python deps
└── README.md              # This file
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | JWT signing key | Required |
| `API_MASTER_KEY` | API master key | Required |
| `DATABASE_URL` | Database connection | sqlite:///./omni_genesis.db |
| `CORS_ORIGINS` | Allowed CORS origins | http://localhost:3000 |
| `LOG_LEVEL` | Logging level | INFO |
| `RATE_LIMIT_PER_MINUTE` | Rate limit | 30 |

### AI Configuration

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key (optional) |
| `ANTHROPIC_API_KEY` | Anthropic API key (optional) |
| `GEMINI_API_KEY` | Google Gemini API key |

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test file
pytest backend/tests/test_auth.py

# Run with verbose output
pytest -v
```

## 🛠️ Development

### Code Style
```bash
# Format code
black backend/
isort backend/

# Lint
flake8 backend/
mypy backend/

# Run pre-commit hooks
pre-commit run --all-files
```

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 📦 Deployment

### Production Checklist
- [ ] Set strong SECRET_KEY
- [ ] Change default API_MASTER_KEY
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable Redis for caching
- [ ] Set up SSL/TLS
- [ ] Configure monitoring
- [ ] Set up log rotation

### Docker Production
```bash
# Build production image
docker build -t omni-genesis:prod -f backend/Dockerfile.prod .

# Run with production config
docker-compose -f docker-compose.prod.yml up -d
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Commit Convention
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code style
- `refactor:` Code refactoring
- `test:` Tests
- `chore:` Maintenance

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [React](https://reactjs.org/) - UI library
- [Gemini](https://deepmind.google/technologies/gemini/) - AI model
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM

## 📞 Support

- 📧 Email: support@omni-genesis.dev
- 💬 Discord: [Join our server](https://discord.gg/omni-genesis)
- 🐛 Issues: [GitHub Issues](https://github.com/icezingza/Project-Omni-Genesis/issues)

---

<p align="center">
  <i>"In the void, we find truth."</i>
</p>
