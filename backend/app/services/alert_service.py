import logging
from datetime import datetime, timedelta
from app.models.database import get_messages_collection

logger = logging.getLogger(__name__)

class AlertService:
    def __init__(self):
        self.STRESS_THRESHOLD = 0.35 # 35% sentiment score
        self.DURATION_DAYS = 3
        
    async def check_user_safety(self, user_id: str, user_email: str = "user@example.com"):
        """Check if user sentiment has been consistently low for 3 days."""
        try:
            coll = get_messages_collection()
            three_days_ago = datetime.utcnow() - timedelta(days=self.DURATION_DAYS)
            
            # Fetch user's sentiment scores for the last 3 days
            cursor = coll.find(
                {
                    "user_id": user_id,
                    "role": "user",
                    "timestamp": {"$gte": three_days_ago},
                    "sentiment_score": {"$ne": None}
                }
            ).sort("timestamp", -1)
            
            messages = await cursor.to_list(length=100)
            
            if not messages:
                return False
                
            # Calculate average sentiment
            scores = [msg["sentiment_score"] for msg in messages]
            avg_sentiment = sum(scores) / len(scores)
            
            # Trigger alert if below threshold
            if avg_sentiment < self.STRESS_THRESHOLD:
                self.send_mock_email(user_email, avg_sentiment)
                return True
                
            return False
        except Exception as e:
            logger.error(f"Error checking safety for {user_id}: {e}")
            return False

    def send_mock_email(self, email: str, score: float):
        """Simulate sending an email alert."""
        print("\n" + "="*50)
        print("🚨  SAFETY ALERT: CRITICAL STRESS DETECTED")
        print("="*50)
        print(f"To: {email}")
        print(f"Subject: Aura AI - Check-in required")
        print(f"Alert: User has maintained low sentiment ({score:.2f}) for 3+ days.")
        print("Action: Automated mental health check-in recommended.")
        print("="*50 + "\n")
        logger.warning(f"Safety alert triggered for {email} (Score: {score:.2f})")

alert_service = AlertService()
