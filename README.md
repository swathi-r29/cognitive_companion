# Cognitive Mood: AI-Based Mental Health Companion

## Overview
Cognitive Mood is an advanced AI companion designed to support mental health through emotion-aware conversations and real-time analytics. It uses cutting-edge NLP models to detect stress, anxiety, and depression patterns, providing empathetic support while maintaining strict safety guardrails.

## Features
- **Emotion-Aware Chat**: Real-time conversation with granular emotion detection (28 categories).
- **Health Dashboard**: Visualize mood trends, stress levels, and cognitive load over time.
- **Safety Guardrails**: Automated crisis detection and multi-layer response filtering to prevent harmful advice.
- **Cognitive Analytics**: Tracking emotional drift and burnout risks.

## Tech Stack
- **Frontend**: React 18, Tailwind CSS, Recharts, Framer Motion.
- **Backend**: FastAPI, WebSockets, SQLAlchemy.
- **AI/ML**: Transformers (BERT, RoBERTa), GPT-4/Claude (via API).
- **Database**: PostgreSQL.
- **Auth**: Firebase.

## Setup Instructions

### Backend
1. Navigate to `backend/`
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the server: `uvicorn app.main:app --reload`

### Frontend
1. Navigate to `frontend/`
2. Install dependencies: `npm install`
3. Run the dev server: `npm run dev`

## Innovation Points (IEEE/Research)
- **Temporal Emotional Drift**: A novel approach to tracking psychological decline over time using vector similarity baselines.
- **Pre-emptive Crisis Routing**: Bypassing generative LLMs for high-risk inputs to ensure safety.
- **Multimodal Ready**: Architecture designed for future integration of voice and facial expression analysis.

---
*Disclaimer: This tool is for support purposes only and does not provide medical diagnosis or treatment.*
