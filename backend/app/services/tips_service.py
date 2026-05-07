import random

class TipsService:
    def __init__(self):
        # Mapping categories to specific actionable advice
        self.tips = {
            "supportive": [
                "It's okay to not be okay. Remember to be as kind to yourself as you would be to a friend.",
                "Small steps still lead to progress. What's one tiny thing you can do for yourself today?",
                "Taking a break isn't giving up; it's recharging. Your energy is valuable.",
                "You don't have to carry everything at once. What can you set down for just 5 minutes?"
            ],
            "grounding": [
                "When things feel chaotic, try the 5-4-3-2-1 technique: 5 things you see, 4 you feel, 3 you hear...",
                "Take a deep breath. Inhale for 4, hold for 4, exhale for 4. Repeat until you feel centered.",
                "Physical movement can help clear mental fog. Try a 2-minute stretch or a quick walk.",
                "Focus on your feet touching the ground. You are here, you are safe, and you are capable."
            ],
            "calming": [
                "Your thoughts are like clouds; let them pass through without holding onto them.",
                "Try minimizing screen time for the next hour. Let your mind rest in the quiet.",
                "Sip some warm water or tea. Focus entirely on the temperature and the taste.",
                "Anxiety is a messenger, but it doesn't always tell the truth. Challenge one 'what-if' with a 'what-is'."
            ],
            "encouraging": [
                "Success is built on small wins. Celebrate what you accomplished today, no matter the size!",
                "You have a unique strength that the world needs. Keep leaning into your passions.",
                "Positivity is a muscle. You're doing a great job at strengthening your emotional health.",
                "Look at how far you've come. Your growth is visible and meaningful."
            ],
            "neutral": [
                "Today is a clean slate. How do you want to define your focus for the next few hours?",
                "Remember to stay hydrated! A clear body often leads to a clearer mind.",
                "Take a moment to notice one beautiful thing around you that you usually overlook.",
                "Reflection is the key to awareness. What's one thing you learned about yourself today?"
            ]
        }

    def get_tip(self, style: str):
        """Get a random tip based on the response style."""
        category_tips = self.tips.get(style, self.tips["neutral"])
        return random.choice(category_tips)

tips_service = TipsService()
