# Omni-Genesis Architecture

## High-level design

```text
Frontend (React/Next.js)
├─ User Interface
├─ Voice Input/Output
└─ Emotion Visualization

API Gateway (FastAPI)
├─ Authentication (JWT)
├─ Rate Limiting
└─ Request Routing

Core Services
├─ Emotion Detection Service
│  ├─ Golden Ratio Analyzer
│  ├─ Thai NLP Engine
│  └─ Context Manager
├─ Response Generation Service
│  ├─ LLM Integration
│  ├─ Thai Language Model
│  └─ Personality Engine (NaMo)
└─ Voice Service
   ├─ TTS
   ├─ STT
   └─ Voice Cloning

Data Layer
├─ PostgreSQL
├─ Redis
└─ Vector DB

Monitoring
├─ Prometheus
├─ Grafana
└─ Sentry
```

## Current implementation status

- ✅ FastAPI gateway with JWT + rate limiting.
- ✅ Golden Ratio emotion analyzer endpoint (`/api/emotion/analyze`).
- ✅ Core chat endpoint integrated with NRE processing.
- 🚧 Voice and full observability stack still planned.
