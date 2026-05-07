from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    db = None

    async def connect(self):
        """Establish connection to MongoDB Atlas"""
        try:
            self.client = AsyncIOMotorClient(settings.MONGODB_URL)
            # Specify the database name explicitly
            self.db = self.client.get_database("cognitive_mood")
            # Verify connection
            await self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB Atlas")
        except Exception as e:
            logger.error(f"Could not connect to MongoDB: {e}")
            raise e

    async def close(self):
        """Close connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

# Global database instance
db = Database()

# --- MongoDB Models (Pydantic) ---

class User(BaseModel):
    firebase_uid: str
    email: str
    name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Message(BaseModel):
    user_id: str  # Using Firebase UID or MongoDB ObjectId string
    role: str     # 'user' or 'bot'
    content: str
    emotion: Optional[str] = None
    sentiment_score: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class DailyMetric(BaseModel):
    user_id: str
    date: datetime = Field(default_factory=datetime.utcnow)
    avg_stress: float
    dominant_emotion: str
    cognitive_load: Optional[float] = None

# Helper to get collections
def get_users_collection():
    return db.db.users

def get_messages_collection():
    return db.db.messages

def get_metrics_collection():
    return db.db.daily_metrics
