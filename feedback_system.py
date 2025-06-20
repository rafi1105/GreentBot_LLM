"""
Simple feedback system for Green University Chatbot
"""

class FeedbackLearningSystem:
    def __init__(self):
        self.feedback_data = []
    
    def get_improved_response_suggestion(self, user_input):
        """Return None since no improved responses available yet"""
        return None
    
    def get_pattern_confidence(self, user_input):
        """Return default confidence"""
        return 0.5
    
    def record_feedback(self, user_question, bot_answer, feedback_type, session_id=None):
        """Record feedback for future learning"""
        feedback_entry = {
            'question': user_question,
            'answer': bot_answer,
            'feedback': feedback_type,
            'session': session_id
        }
        self.feedback_data.append(feedback_entry)
        return {"status": "success", "message": "Feedback recorded"}
    
    def get_feedback_stats(self):
        """Get basic feedback statistics"""
        return {
            "total_feedback": len(self.feedback_data),
            "positive_feedback": len([f for f in self.feedback_data if f['feedback'] == 'like']),
            "negative_feedback": len([f for f in self.feedback_data if f['feedback'] == 'dislike'])
        }
