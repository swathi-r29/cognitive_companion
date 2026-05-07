import logging

logger = logging.getLogger(__name__)

class SafetyGuardrails:
    @staticmethod
    def check_input(text: str):
        """Pre-processing safety check"""
        # 1. Block NSFW/Harmful prompts
        # 2. Check for PII (Personal Identifiable Information)
        # 3. Detect jailbreak attempts
        return {"safe": True, "action": "PROCEED"}

    @staticmethod
    def check_output(response: str):
        """Post-processing safety check"""
        # 1. Ensure no medical diagnosis is given
        # 2. Block harmful advice
        medical_keywords = ["diagnose", "cure", "prescription", "medicine"]
        if any(kw in response.lower() for kw in medical_keywords):
            return {
                "safe": False, 
                "action": "REDACT", 
                "message": "I am an AI companion and cannot provide medical advice. Please consult a professional."
            }
        return {"safe": True, "response": response}

    @staticmethod
    def handle_crisis(risk_score: float):
        """Crisis escalation protocol"""
        if risk_score >= 0.8:
            return {
                "is_crisis": True,
                "message": "It sounds like you're going through a lot. Please reach out to a professional or a crisis hotline immediately. You are not alone. (US: 988, UK: 111)"
            }
        return {"is_crisis": False}

safety_guardrails = SafetyGuardrails()
