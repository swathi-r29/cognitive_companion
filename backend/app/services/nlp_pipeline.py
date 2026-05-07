from transformers import pipeline
import torch
import logging

logger = logging.getLogger(__name__)

class NLPPipeline:
    def __init__(self):
        # We initialize pipelines lazily or on startup
        # For a production/industry level app, we should use a singleton pattern
        self.device = 0 if torch.cuda.is_available() else -1
        self.emotion_classifier = None
        self.sentiment_analyzer = None
        self.risk_detector = None

    def load_models(self):
        """Pre-load models to memory"""
        try:
            logger.info("Loading Advanced RoBERTa NLP models (GoEmotions)...")
            # Using RoBERTa-based GoEmotions model (28 emotions)
            self.emotion_classifier = pipeline(
                "text-classification", 
                model="SamLowe/roberta-base-go_emotions", 
                top_k=1,
                device=self.device
            )
            # Using RoBERTa for sentiment
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis", 
                model="cardiffnlp/twitter-roberta-base-sentiment", 
                device=self.device
            )
            logger.info("Advanced models loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading models: {e}")

    def analyze_text(self, text: str):
        """Run full analysis pipeline on text"""
        if not self.emotion_classifier:
            self.load_models()

        # 1. Emotion detection (28 nuanced labels)
        emotions_output = self.emotion_classifier(text)
        raw_emotion = emotions_output[0][0]['label']
        confidence = emotions_output[0][0]['score']
        
        # 2. Sentiment detection & Normalization
        sentiment_output = self.sentiment_analyzer(text)
        sentiment_label = sentiment_output[0]['label']
        sentiment_conf = sentiment_output[0]['score']
        
        # Map labels to 0-1 scale: 0=Negative, 0.5=Neutral, 1.0=Positive
        if sentiment_label == 'LABEL_0': # Negative
            normalized_sentiment = 1.0 - sentiment_conf # High confidence neg = low score
        elif sentiment_label == 'LABEL_1': # Neutral
            normalized_sentiment = 0.5
        else: # LABEL_2 (Positive)
            normalized_sentiment = sentiment_conf # High confidence pos = high score
        
        # 3. Comprehensive Style Mapping (28 emotions -> response tones)
        style_map = {
            # Low Energy / Supportive
            "sadness": "supportive", "grief": "supportive", "disappointment": "supportive", 
            "remorse": "supportive", "embarrassment": "supportive",
            
            # High Energy / Grounding
            "anger": "grounding", "annoyance": "grounding", "disapproval": "grounding", "disgust": "grounding",
            
            # Anxious / Calming
            "fear": "calming", "nervousness": "calming", "confusion": "calming",
            
            # Positive / Encouraging
            "joy": "encouraging", "love": "encouraging", "admiration": "encouraging", 
            "approval": "encouraging", "caring": "encouraging", "excitement": "encouraging", 
            "gratitude": "encouraging", "optimism": "encouraging", "pride": "encouraging", "relief": "encouraging",
            
            # Neutral / Curious
            "curiosity": "neutral", "realization": "neutral", "surprise": "neutral", "amusement": "neutral", "desire": "neutral"
        }
        
        # 4. Crisis Keyword Check (Final Safety layer)
        text_lower = text.lower()
        if any(w in text_lower for w in ["suicide", "kill myself", "end it"]):
            raw_emotion = "crisis"
            style = "crisis"
        else:
            style = style_map.get(raw_emotion, "neutral")

        return {
            "emotion": raw_emotion,
            "style": style,
            "emotion_score": confidence,
            "sentiment": sentiment_label,
            "sentiment_score": normalized_sentiment,
            "risk_score": 1.0 if raw_emotion == "crisis" else 0.0
        }

    def calculate_risk_score(self, text: str):
        """Detect self-harm or crisis patterns"""
        crisis_keywords = ["suicide", "kill myself", "end it all", "harm myself", "worthless"]
        text_lower = text.lower()
        if any(keyword in text_lower for keyword in crisis_keywords):
            return 1.0
        return 0.0

# Singleton instance
nlp_pipeline = NLPPipeline()
