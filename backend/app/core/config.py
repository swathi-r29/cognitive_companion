from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Cognitive Mood"
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017/cognitive_mood")
    
    # Firebase Config (Provided by User)
    FIREBASE_API_KEY: str = "AIzaSyA3TLYqN77I2_V83dy3hIWLaML9iUdhl6g"
    FIREBASE_PROJECT_ID: str = "cognitive-mood"
    FIREBASE_AUTH_DOMAIN: str = "cognitive-mood.firebaseapp.com"
    
    # AI Config
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    class Config:
        case_sensitive = True

settings = Settings()
