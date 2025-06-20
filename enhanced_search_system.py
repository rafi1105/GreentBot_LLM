#!/usr/bin/env python3
"""
Enhanced Search System for Green University Chatbot
- Searches ALL JSON data comprehensively
- Learns from user feedback (likes/dislikes)
- Permanently removes disliked answers and keywords
- Provides diverse responses based on complete data analysis
"""

import json
import numpy as np
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import datetime
from typing import Dict, List, Any, Optional

class EnhancedChatbotSearchSystem:
    def __init__(self, data_file_path: str = "ndata.json"):
        """Initialize the enhanced search system with comprehensive data analysis"""
        
        # NLP setup
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english')) | {"university", "please", "can"}
        
        # File paths
        self.data_file_path = data_file_path
        self.feedback_file_path = "user_feedback_data.json"
        self.disliked_answers_file = "disliked_answers.json"
        self.blocked_keywords_file = "blocked_keywords.json"
        
        # Load and process data
        self.load_data()
        self.load_feedback_data()
        self.preprocess_all_data()
        self.train_models()
        
        print(f"✅ Enhanced Search System initialized with {len(self.data)} total data points")
        print(f"📊 Disliked answers blocked: {len(self.disliked_answers)}")
        print(f"🚫 Blocked keywords: {len(self.blocked_keywords)}")
    
    def load_data(self):
        """Load JSON data with fallback paths"""
        possible_paths = [
            self.data_file_path,
            "enhanced_ndata.json",
            "react-chatbot/enhanced_ndata.json",
            "react-chatbot/ndata.json"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                with open(path, "r", encoding='utf-8') as f:
                    self.data = json.load(f)
                self.data_file_path = path
                break
        else:
            raise FileNotFoundError("No data file found!")
    
    def load_feedback_data(self):
        """Load user feedback and dislike data"""
        # Load disliked answers
        try:
            with open(self.disliked_answers_file, "r", encoding='utf-8') as f:
                self.disliked_answers = json.load(f)
        except FileNotFoundError:
            self.disliked_answers = []
        
        # Load blocked keywords
        try:
            with open(self.blocked_keywords_file, "r", encoding='utf-8') as f:
                self.blocked_keywords = json.load(f)
        except FileNotFoundError:
            self.blocked_keywords = set()
        else:
            self.blocked_keywords = set(self.blocked_keywords)
        
        # Load general feedback
        try:
            with open(self.feedback_file_path, "r", encoding='utf-8') as f:
                self.feedback_data = json.load(f)
        except FileNotFoundError:
            self.feedback_data = []
    
    def save_feedback_data(self):
        """Save all feedback data to files"""
        # Save disliked answers
        with open(self.disliked_answers_file, "w", encoding='utf-8') as f:
            json.dump(self.disliked_answers, f, indent=2, ensure_ascii=False)
        
        # Save blocked keywords
        with open(self.blocked_keywords_file, "w", encoding='utf-8') as f:
            json.dump(list(self.blocked_keywords), f, indent=2, ensure_ascii=False)
        
        # Save general feedback
        with open(self.feedback_file_path, "w", encoding='utf-8') as f:
            json.dump(self.feedback_data, f, indent=2, ensure_ascii=False)
      def preprocess(self, text: str) -> str:
        """Enhanced text preprocessing"""
        if not text:
            return ""
        
        text = text.lower().strip()
        text = ''.join([c for c in text if c.isalnum() or c.isspace()])
        words = [self.lemmatizer.lemmatize(word) for word in text.split() 
                if word not in self.stop_words and word not in self.blocked_keywords]
        return ' '.join(words)
    
    def preprocess_all_data(self):
        """Preprocess all questions, answers, and keywords with improved blocking"""
        self.questions = []
        self.answers = []
        self.keywords_list = []
        self.categories = []
        
        for i, item in enumerate(self.data):
            # Skip if this SPECIFIC answer is disliked
            if any(disliked['answer'] == item['answer'] for disliked in self.disliked_answers):
                continue
            
            # Preprocess question and keywords (don't filter keywords globally)
            processed_question = self.preprocess(item["question"])
            processed_keywords = [self.preprocess(kw) for kw in item.get("keywords", [])]
            
            # Only skip if the specific answer+keywords combination was disliked
            # Don't block all items that contain any blocked keyword
            
            self.questions.append(processed_question)
            self.answers.append(item["answer"])
            self.keywords_list.append(processed_keywords)
            
            # Determine category
            if "categories" in item and item["categories"]:
                self.categories.append(item["categories"][0])
            else:
                self.categories.append(self._auto_categorize(item.get("keywords", [])))
    
    def _auto_categorize(self, keywords: List[str]) -> str:
        """Auto-categorize based on keywords"""
        keywords_lower = [kw.lower() for kw in keywords]
        
        if any(word in keywords_lower for word in ["fee", "tuition", "cost", "price"]):
            return "fees"
        elif any(word in keywords_lower for word in ["admission", "requirement", "apply", "enrollment"]):
            return "admission"
        elif any(word in keywords_lower for word in ["program", "course", "department", "cse", "bba"]):
            return "programs"
        elif any(word in keywords_lower for word in ["contact", "phone", "email", "address"]):
            return "contact"
        else:
            return "general"
    
    def train_models(self):
        """Train ML models on filtered data"""
        if not self.questions:
            print("⚠️ No valid questions after filtering disliked content!")
            return
        
        # TF-IDF Vectorization
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 3), 
            max_features=10000, 
            min_df=1, 
            max_df=0.95
        )
        self.X = self.vectorizer.fit_transform(self.questions)
        
        # Category Classification
        self.label_encoder = LabelEncoder()
        encoded_categories = self.label_encoder.fit_transform(self.categories)
          # Train classifier
        if len(set(encoded_categories)) > 1:  # Need at least 2 categories
            X_train, X_test, y_train, y_test = train_test_split(
                self.X, encoded_categories, test_size=0.2, random_state=42
            )
            self.category_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
            self.category_classifier.fit(X_train, y_train)
            accuracy = self.category_classifier.score(X_test, y_test)
            print(f"🤖 ML Model trained with accuracy: {accuracy:.3f}")
        else:
            self.category_classifier = None
            print("⚠️ Not enough categories for classification")
    
    def comprehensive_search(self, user_input: str, threshold: float = 0.25) -> Dict[str, Any]:
        """
        COMPREHENSIVE SEARCH THROUGH ALL AVAILABLE DATA WITH IMPROVED BLOCKING
        - Analyzes every non-disliked item in JSON
        - Finds multiple candidates and returns best non-blocked answer
        - Only blocks specific answers, not all related keywords
        """
        
        if not self.questions:
            return self._fallback_response("No data available after filtering", user_input)
        
        processed_input = self.preprocess(user_input)
        
        # Handle special cases
        special_response = self._handle_special_cases(user_input)
        if special_response:
            return special_response
        
        # STEP 1: Vectorize user input
        try:
            user_vec = self.vectorizer.transform([processed_input])
        except Exception:
            return self._fallback_response("Processing error", user_input)
        
        # STEP 2: Category prediction
        predicted_category = "general"
        category_confidence = 0.5
        
        if self.category_classifier:
            try:
                predicted_category_encoded = self.category_classifier.predict(user_vec)[0]
                predicted_category = self.label_encoder.inverse_transform([predicted_category_encoded])[0]
                category_confidence = np.max(self.category_classifier.predict_proba(user_vec))
            except Exception:
                pass
        
        # STEP 3: ANALYZE ALL AVAILABLE DATA POINTS
        all_similarities = cosine_similarity(user_vec, self.X).flatten()
        
        # STEP 4: ENHANCED SCORING SYSTEM
        enhanced_scores = np.zeros(len(self.questions))
        input_words = set(processed_input.split())
        
        for i in range(len(self.questions)):
            # Base similarity score
            base_score = all_similarities[i]
            
            # Exact question matching (highest priority)
            exact_question_bonus = 0.0
            processed_question = self.questions[i]
            if processed_input == processed_question:
                exact_question_bonus = 1.0
            elif len(input_words.intersection(set(processed_question.split()))) >= len(input_words) * 0.8:
                exact_question_bonus = 0.8
            
            # Keyword matching
            item_keywords = set(self.keywords_list[i])
            exact_keyword_matches = len(input_words.intersection(item_keywords))
            keyword_score = exact_keyword_matches / max(len(item_keywords), 1) if item_keywords else 0
            
            # Category bonus
            category_bonus = 0.3 if self.categories[i] == predicted_category else 0.0
            
            # Question word overlap
            question_words = set(processed_question.split())
            question_overlap = len(input_words.intersection(question_words))
            question_bonus = question_overlap / max(len(question_words), 1) if question_words else 0
            
            # Calculate final score with exact question priority
            if exact_question_bonus > 0.7:
                enhanced_scores[i] = (
                    exact_question_bonus * 0.6 +
                    base_score * 0.25 +
                    keyword_score * 0.1 +
                    category_bonus * 0.05
                )
            else:
                enhanced_scores[i] = (
                    base_score * 0.4 +
                    category_bonus * 0.2 +
                    keyword_score * 0.25 +
                    question_bonus * 0.15
                )
        
        # STEP 5: Find MULTIPLE best matches and select first non-blocked
        if len(enhanced_scores) == 0:
            return self._fallback_response("No matches found", user_input)
        
        # Get top 5 candidates sorted by score
        sorted_indices = np.argsort(enhanced_scores)[::-1]
        top_candidates = sorted_indices[:5]
        
        # Find the best non-blocked answer
        for idx in top_candidates:
            candidate_answer = self.answers[idx]
            candidate_score = enhanced_scores[idx]
            
            # Check if this specific answer is blocked
            is_blocked = any(disliked['answer'] == candidate_answer for disliked in self.disliked_answers)
            
            if not is_blocked and candidate_score >= threshold:
                # STEP 6: Confidence calculation
                final_confidence = candidate_score * (0.7 + category_confidence * 0.3)
                
                return {
                    "answer": candidate_answer,
                    "confidence": float(min(final_confidence, 1.0)),
                    "source": "comprehensive_search",
                    "method": "enhanced_ml_analysis",
                    "analyzed_items": len(self.questions),
                    "total_original_items": len(self.data),
                    "filtered_out": len(self.data) - len(self.questions),
                    "predicted_category": str(predicted_category),
                    "category_confidence": float(category_confidence),
                    "base_similarity": float(all_similarities[idx]),
                    "enhanced_score": float(candidate_score),
                    "exact_match": bool(enhanced_scores[idx] > 0.7),
                    "candidate_rank": int(np.where(top_candidates == idx)[0][0] + 1),
                    "alternatives_checked": len(top_candidates)
                }
        
        # If all top candidates are blocked, return fallback
        blocked_count = sum(1 for idx in top_candidates 
                          if any(disliked['answer'] == self.answers[idx] 
                                for disliked in self.disliked_answers))
        
        return self._fallback_response("All best matches are blocked by user feedback", user_input, {
            "best_score": float(enhanced_scores[sorted_indices[0]]),
            "predicted_category": str(predicted_category),
            "analyzed_items": len(self.questions),
            "blocked_candidates": blocked_count,
            "total_candidates_checked": len(top_candidates)
        })
    
    def _handle_special_cases(self, user_input: str) -> Optional[Dict[str, Any]]:
        """Handle special command cases"""
        user_lower = user_input.lower()
        
        if 'time' in user_lower:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return {
                "answer": f"The current time is {now}.",
                "confidence": 1.0,
                "source": "special_command",
                "method": "direct_response",
                "analyzed_items": 0
            }
        
        if any(phrase in user_lower for phrase in ["how are you", "how r u"]):
            return {
                "answer": "I'm doing well, thank you! How can I help you with information about Green University?",
                "confidence": 1.0,
                "source": "greeting",
                "method": "direct_response",
                "analyzed_items": 0
            }
        
        return None
    
    def _fallback_response(self, reason: str, user_input: str, extra_info: Dict = None) -> Dict[str, Any]:
        """Enhanced fallback response"""
        return {            "answer": ("I don't have specific information about that. "
                      "You can contact Green University directly at: "
                      "Phone: +880-2-7791071-5, Admission: 01775234234, "
                      "Email: info@green.edu.bd, Website: https://www.green.edu.bd/"),
            "confidence": 0.15,
            "source": "fallback",
            "method": "no_match_found",
            "reason": reason,
            "analyzed_items": len(self.questions) if hasattr(self, 'questions') else 0,
            **(extra_info or {})
        }
    
    def record_user_feedback(self, user_question: str, bot_answer: str, feedback_type: str, 
                           answer_index: Optional[int] = None) -> Dict[str, Any]:
        """
        Record user feedback and handle dislikes by removing answers and keywords
        """
        timestamp = datetime.datetime.now().isoformat()
        
        # Record general feedback
        feedback_entry = {
            'timestamp': timestamp,
            'question': user_question,
            'answer': bot_answer,
            'feedback': feedback_type,
            'answer_index': answer_index
        }
        self.feedback_data.append(feedback_entry)
        
        # Handle DISLIKE feedback - permanently remove
        if feedback_type == 'dislike':
            # Add to disliked answers
            dislike_entry = {
                'answer': bot_answer,
                'question': user_question,
                'timestamp': timestamp,
                'blocked_permanently': True
            }
            self.disliked_answers.append(dislike_entry)
            
            # Find and block keywords from this answer
            for item in self.data:
                if item['answer'] == bot_answer:
                    # Add keywords to blocked list
                    for keyword in item.get('keywords', []):
                        self.blocked_keywords.add(keyword.lower())
                    
                    print(f"🚫 Blocked answer and {len(item.get('keywords', []))} keywords")
                    break
            
            # Retrain models without this data
            self.preprocess_all_data()
            self.train_models()
            
            # Save all feedback data
            self.save_feedback_data()
            
            return {
                "status": "success",
                "message": "Answer disliked and permanently removed from future responses",
                "blocked_keywords": len(self.blocked_keywords),
                "blocked_answers": len(self.disliked_answers)
            }
        
        # Handle LIKE feedback
        elif feedback_type == 'like':
            # Save feedback but no action needed
            self.save_feedback_data()
            
            return {
                "status": "success", 
                "message": "Positive feedback recorded"
            }
        
        return {"status": "success", "message": "Feedback recorded"}
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        return {
            "total_original_data": len(self.data),
            "available_data": len(self.questions) if hasattr(self, 'questions') else 0,
            "disliked_answers": len(self.disliked_answers),
            "blocked_keywords": len(self.blocked_keywords),
            "total_feedback": len(self.feedback_data),
            "positive_feedback": len([f for f in self.feedback_data if f['feedback'] == 'like']),
            "negative_feedback": len([f for f in self.feedback_data if f['feedback'] == 'dislike']),
            "filtering_active": len(self.disliked_answers) > 0 or len(self.blocked_keywords) > 0,
            "ml_model_active": hasattr(self, 'category_classifier') and self.category_classifier is not None
        }
    
    def reset_all_feedback(self) -> Dict[str, str]:
        """Reset all feedback data (for testing purposes)"""
        self.disliked_answers = []
        self.blocked_keywords = set()
        self.feedback_data = []
        
        # Remove files
        for file_path in [self.feedback_file_path, self.disliked_answers_file, self.blocked_keywords_file]:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Retrain with all data
        self.preprocess_all_data()
        self.train_models()
        
        return {"status": "success", "message": "All feedback data reset and models retrained"}

# Global instance
enhanced_search_system = None

def initialize_enhanced_system(data_file: str = "ndata.json"):
    """Initialize the enhanced search system"""
    global enhanced_search_system
    enhanced_search_system = EnhancedChatbotSearchSystem(data_file)
    return enhanced_search_system

def search_with_learning(user_input: str) -> Dict[str, Any]:
    """Main search function with learning capabilities"""
    global enhanced_search_system
    if not enhanced_search_system:
        enhanced_search_system = initialize_enhanced_system()
    
    return enhanced_search_system.comprehensive_search(user_input)

def record_feedback(user_question: str, bot_answer: str, feedback_type: str) -> Dict[str, Any]:
    """Record user feedback"""
    global enhanced_search_system
    if not enhanced_search_system:
        enhanced_search_system = initialize_enhanced_system()
    
    return enhanced_search_system.record_user_feedback(user_question, bot_answer, feedback_type)

def get_enhanced_stats() -> Dict[str, Any]:
    """Get system statistics"""
    global enhanced_search_system
    if not enhanced_search_system:
        enhanced_search_system = initialize_enhanced_system()
    
    return enhanced_search_system.get_system_stats()

if __name__ == "__main__":
    # Test the enhanced system
    system = initialize_enhanced_system()
    
    print("\n🔍 Testing Enhanced Search System:")
    
    # Test searches
    test_queries = [
        "What is the tuition fee for CSE?",
        "How to apply for admission?",
        "Contact information",
        "What time is it?"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        result = system.comprehensive_search(query)
        print(f"💬 Answer: {result['answer'][:100]}...")
        print(f"🎯 Confidence: {result['confidence']:.2f}")
        print(f"📊 Analyzed: {result['analyzed_items']} items")
    
    # Test feedback
    print(f"\n📊 System Stats: {system.get_system_stats()}")
