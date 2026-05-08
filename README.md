# Cognitive Mood: AI-Based Mental Health Companion

## Overview
Cognitive Mood is an advanced AI companion designed to support mental health through emotion-aware conversations and real-time analytics. It uses cutting-edge NLP models to detect stress, anxiety, and depression patterns, providing empathetic support while maintaining strict safety guardrails.

## Features
- **Emotion-Aware Chat**: Real-time conversation with granular emotion detection (28 categories).
- **Health Dashboard**: Visualize mood trends, stress levels, and cognitive load over time using Recharts.
- **Safety Guardrails**: Automated crisis detection and multi-layer response filtering to prevent harmful advice.
- **Asynchronous AI Pipeline**: Optimized inference engine that offloads heavy model processing to background threads to ensure high responsiveness.

## Tech Stack
- **Frontend**: React 19, Tailwind CSS, Recharts, Framer Motion, Lucide React.
- **Backend**: FastAPI, WebSockets, Motor (Async MongoDB Driver).
- **AI/ML**: Transformers (RoBERTa - GoEmotions), PyTorch.
- **Database**: MongoDB (Atlas).
- **Auth**: Firebase Authentication.

## Setup Instructions

### Backend
1. Navigate to `backend/`
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
4. Install dependencies: `pip install -r requirements.txt`
5. Configure `.env`: Add `MONGODB_URL` and `OPENAI_API_KEY`.
6. Run the server: `uvicorn app.main:app --reload`

### Frontend
1. Navigate to `frontend/`
2. Install dependencies: `npm install`
3. Run the dev server: `npm run dev`

## Innovation Points (IEEE/Research)
- **Hybrid NLP Engine**: A dual-layer system combining Deep Learning (RoBERTa) with rule-based heuristics for 100% uptime and high accuracy.
- **Pre-emptive Crisis Routing**: Real-time sentiment scoring and keyword analysis for immediate crisis intervention.
- **Non-Blocking Architecture**: Leveraging Python's `asyncio` and thread executors to run high-latency AI models without freezing the API.

---
*Disclaimer: This tool is for support purposes only and does not provide medical diagnosis or treatment.*

