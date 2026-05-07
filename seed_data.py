import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv

load_dotenv("backend/.env")

async def seed_data():
    uri = os.getenv("MONGODB_URL")
    client = AsyncIOMotorClient(uri)
    db = client.get_database("cognitive_mood")
    messages = db.messages

    user_id = "123"
    emotions = ["joy", "sadness", "fear", "anger", "optimism", "nervousness", "admiration"]
    
    print("Clearing old data (optional)...")
    # await messages.delete_many({"user_id": user_id})

    print(f"Seeding mock data for the last 7 days to: {uri}")
    
    mock_messages = []
    
    for i in range(7, -1, -1): # From 7 days ago to today
        date = datetime.utcnow() - timedelta(days=i)
        
        # Add 3-8 messages per day
        num_messages = random.randint(3, 8)
        
        for _ in range(num_messages):
            emotion = random.choice(emotions)
            # User Message
            mock_messages.append({
                "user_id": user_id,
                "role": "user",
                "content": f"Mock message for {date.date()}",
                "emotion": emotion,
                "sentiment_score": random.uniform(0.1, 0.9),
                "timestamp": date + timedelta(hours=random.randint(0, 23))
            })
            # Bot Response
            mock_messages.append({
                "user_id": user_id,
                "role": "bot",
                "content": "I'm here to listen.",
                "emotion": emotion,
                "timestamp": date + timedelta(hours=random.randint(0, 23), minutes=1)
            })

    if mock_messages:
        await messages.insert_many(mock_messages)
        print(f"✅ Successfully inserted {len(mock_messages)} mock messages!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_data())
