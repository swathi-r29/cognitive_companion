from fastapi import APIRouter
from app.models.database import get_messages_collection
from app.services.tips_service import tips_service
from datetime import datetime, timedelta
import logging

router = APIRouter(prefix="/analytics", tags=["analytics"])
logger = logging.getLogger(__name__)

@router.get("/mood-distribution/{user_id}")
async def get_mood_distribution(user_id: str):
    """Get the count of each emotion for a specific user."""
    try:
        coll = get_messages_collection()
        pipeline = [
            {"$match": {"user_id": user_id, "role": "user", "emotion": {"$ne": None}}},
            {"$group": {"_id": "$emotion", "count": {"$sum": 1}}},
            {"$project": {"name": "$_id", "value": "$count", "_id": 0}}
        ]
        cursor = coll.aggregate(pipeline)
        results = await cursor.to_list(length=100)
        return results
    except Exception as e:
        logger.error(f"Error fetching mood distribution: {e}")
        return []

@router.get("/mood-trends/{user_id}")
async def get_mood_trends(user_id: str):
    """Get mood trends over the last 7 days."""
    try:
        coll = get_messages_collection()
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        
        pipeline = [
            {
                "$match": {
                    "user_id": user_id, 
                    "role": "user", 
                    "timestamp": {"$gte": seven_days_ago}
                }
            },
            {
                "$group": {
                    "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}},
                    "count": {"$sum": 1},
                    "avg_sentiment": {"$avg": "$sentiment_score"}
                }
            },
            {"$sort": {"_id": 1}},
            {
                "$project": {
                    "date": "$_id",
                    "messages": "$count",
                    "sentiment": {"$multiply": ["$avg_sentiment", 100]}, # Convert to 0-100 scale
                    "_id": 0
                }
            }
        ]
        cursor = coll.aggregate(pipeline)
        results = await cursor.to_list(length=100)
        return results
    except Exception as e:
        logger.error(f"Error fetching mood trends: {e}")
        return []

@router.get("/summary/{user_id}")
async def get_summary(user_id: str):
    """Get high-level insights for the dashboard."""
    try:
        coll = get_messages_collection()
        
        # Total messages
        total_messages = await coll.count_documents({"user_id": user_id, "role": "user"})
        
        # Dominant emotion
        pipeline = [
            {"$match": {"user_id": user_id, "role": "user", "emotion": {"$ne": None}}},
            {"$group": {"_id": "$emotion", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 1}
        ]
        dominant_cursor = coll.aggregate(pipeline)
        dominant_result = await dominant_cursor.to_list(length=1)
        dominant_emotion = dominant_result[0]["_id"] if dominant_result else "Neutral"
        
        return {
            "total_interactions": total_messages,
            "dominant_emotion": dominant_emotion.capitalize(),
            "status": "Healthy" if dominant_emotion in ["joy", "love", "optimism"] else "Monitoring"
        }
    except Exception as e:
        logger.error(f"Error fetching summary: {e}")
        return {"total_interactions": 0, "dominant_emotion": "N/A", "status": "Unknown"}

@router.get("/daily-tip/{user_id}")
async def get_daily_tip(user_id: str):
    """Provide a personalized tip based on today's dominant emotion."""
    try:
        coll = get_messages_collection()
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Get dominant emotion for today
        pipeline = [
            {
                "$match": {
                    "user_id": user_id, 
                    "role": "user", 
                    "timestamp": {"$gte": today_start}
                }
            },
            {"$group": {"_id": "$emotion", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 1}
        ]
        
        cursor = coll.aggregate(pipeline)
        result = await cursor.to_list(length=1)
        
        # Determine style from emotion
        emotion = result[0]["_id"] if result else "neutral"
        
        # Use simple mapping logic for tip selection
        style_map = {
            "sadness": "supportive", "grief": "supportive", "disappointment": "supportive",
            "anger": "grounding", "annoyance": "grounding",
            "fear": "calming", "nervousness": "calming",
            "joy": "encouraging", "love": "encouraging", "optimism": "encouraging"
        }
        style = style_map.get(emotion, "neutral")
        
        return {
            "tip": tips_service.get_tip(style),
            "category": style.capitalize()
        }
    except Exception as e:
        logger.error(f"Error fetching daily tip: {e}")
        return {"tip": tips_service.get_tip("neutral"), "category": "General"}
