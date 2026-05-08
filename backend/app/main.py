from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.services.nlp_pipeline import nlp_pipeline
from app.services.safety_guardrails import safety_guardrails
from app.services.alert_service import alert_service
from app.models.database import db, get_messages_collection, Message
from app.api.analytics import router as analytics_router
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Cognitive Mood API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(analytics_router, prefix="/api")

# In-memory connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: dict, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(json.dumps(message))

import asyncio

manager = ConnectionManager()

# ── Simple rule-based emotion fallback (works instantly, no download needed) ──
RULE_BASED_EMOTIONS = {
    "sad": ("sadness", "supportive"), "depress": ("sadness", "supportive"),
    "cry": ("sadness", "supportive"), "unhappy": ("sadness", "supportive"),
    "anxious": ("fear", "calming"), "anxiety": ("fear", "calming"),
    "worried": ("fear", "calming"), "nervous": ("fear", "calming"),
    "stress": ("fear", "calming"), "overwhelm": ("fear", "calming"),
    "happy": ("joy", "encouraging"), "great": ("joy", "encouraging"),
    "good": ("joy", "encouraging"), "excited": ("joy", "encouraging"),
    "angry": ("anger", "grounding"), "frustrat": ("anger", "grounding"),
    "tired": ("fatigue", "restorative"), "exhaust": ("fatigue", "restorative"),
    "lonely": ("loneliness", "connecting"), "alone": ("loneliness", "connecting"),
}

BOT_REPLIES = {
    "supportive":    "I'm really sorry you're feeling that way. You're not alone in this, and it takes courage to share. Can you tell me a bit more about what's been happening?",
    "calming":       "I can hear that you're feeling overwhelmed right now. Let's take a breath together. What's been weighing on your mind the most?",
    "encouraging":   "That's wonderful to hear! Positive moments matter. What's been going well for you lately?",
    "grounding":     "It sounds like you're carrying a lot of frustration. That's completely valid. What do you think is at the root of it?",
    "restorative":   "Feeling drained can be really tough. Your rest and recovery matters. Have you been able to take any breaks for yourself?",
    "connecting":    "Loneliness can be really painful. I'm here and I'm listening. What's been making you feel disconnected?",
    "neutral":       "Thank you for sharing that with me. I'm here to listen. How has your day been going overall?",
}

def rule_based_analysis(text: str):
    text_lower = text.lower()
    for keyword, (emotion, style) in RULE_BASED_EMOTIONS.items():
        if keyword in text_lower:
            return {"emotion": emotion, "sentiment": "NEGATIVE", "risk_score": 0.0, "style": style}
    return {"emotion": "neutral", "sentiment": "NEUTRAL", "risk_score": 0.0, "style": "neutral"}

def crisis_keywords_check(text: str):
    crisis_terms = ["suicide", "kill myself", "end it all", "harm myself", "worthless", "don't want to live"]
    return any(term in text.lower() for term in crisis_terms)

@app.on_event("startup")
async def startup_event():
    """Establish DB connection and pre-load NLP models."""
    await db.connect()
    
    async def load_in_background():
        await asyncio.sleep(2)  # Let server boot first
        try:
            # Load models in a separate thread to avoid blocking the event loop
            await asyncio.to_thread(nlp_pipeline.load_models)
        except Exception as e:
            logger.warning(f"NLP model load failed, rule-based fallback will be used: {e}")
    asyncio.create_task(load_in_background())

@app.get("/")
async def root():
    return {"message": "Welcome to Cognitive Mood API", "status": "running"}

@app.get("/api/history/{user_id}")
async def get_history(user_id: str):
    """Fetch recent chat history for a specific user."""
    try:
        coll = get_messages_collection()
        cursor = coll.find({"user_id": user_id}).sort("timestamp", 1).limit(50)
        messages = await cursor.to_list(length=50)
        # Convert ObjectId and datetime for JSON serialization
        for msg in messages:
            msg["_id"] = str(msg["_id"])
            if "timestamp" in msg and msg["timestamp"]:
                msg["timestamp"] = msg["timestamp"].isoformat()
        return messages
    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        return []

@app.websocket("/ws/chat/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            text = message_data.get('content', '').strip()
            if not text:
                continue

            # 1. Crisis check first (always fast, rule-based)
            if crisis_keywords_check(text):
                await manager.send_personal_message({
                    "type": "BOT_RESPONSE",
                    "content": "💙 It sounds like you're going through something incredibly painful right now. Please reach out to a crisis helpline immediately — you don't have to face this alone.\n\n🇮🇳 iCall: 9152987821\n🌍 International: befrienders.org",
                    "metadata": {"emotion": "crisis", "is_crisis": True, "stress_level": "critical"}
                }, user_id)
                continue

            # 2. Try AI pipeline (only if models are loaded)
            analysis = None
            if nlp_pipeline.emotion_classifier:
                try:
                    analysis = await nlp_pipeline.analyze_text(text)
                except Exception as e:
                    logger.warning(f"NLP pipeline error: {e}")

            # 3. Fallback to rule-based if model not ready
            if not analysis:
                analysis = rule_based_analysis(text)

            emotion = analysis.get("emotion", "neutral")
            style = analysis.get("style", "neutral")
            reply = BOT_REPLIES.get(style, BOT_REPLIES["neutral"])

            # 4. Safety check on output
            output_check = safety_guardrails.check_output(reply)
            final_content = output_check.get("response", output_check.get("message", reply))

            stress_level = "high" if emotion in ["fear", "sadness", "crisis"] else "medium" if emotion in ["anger", "fatigue"] else "low"

            # 5. Persist both user and bot messages to MongoDB
            try:
                coll = get_messages_collection()
                # Save user message
                await coll.insert_one(Message(
                    user_id=user_id, role="user", content=text, 
                    emotion=emotion, sentiment_score=analysis.get("sentiment_score")
                ).dict())
                
                # Check for Safety Alerts (Mock Email)
                await alert_service.check_user_safety(user_id)
                
                # Save bot response
                await coll.insert_one(Message(
                    user_id=user_id, role="bot", content=final_content,
                    emotion=emotion
                ).dict())
            except Exception as e:
                logger.warning(f"Failed to persist message to DB: {e}")

            await manager.send_personal_message({
                "type": "BOT_RESPONSE",
                "content": final_content,
                "metadata": {
                    "emotion": emotion,
                    "sentiment": analysis.get("sentiment", "NEUTRAL"),
                    "stress_level": stress_level
                }
            }, user_id)

    except WebSocketDisconnect:
        manager.disconnect(user_id)
        logger.info(f"User {user_id} disconnected")
    except Exception as e:
        logger.error(f"WebSocket error for {user_id}: {e}")
        manager.disconnect(user_id)

@app.on_event("shutdown")
async def shutdown_event():
    await db.close()
