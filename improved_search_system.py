#!/usr/bin/env python3
"""
Improved Enhanced Search System for Green University Chatbot
- Fixed keyword blocking issue
- Finds next best answer when primary choice is blocked
- Only blocks specific answers, not all related keywords
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

class ImprovedChatbotSearchSystem:
    def __init__(self, data_file_path: str = "ndata.json"):
        """Initialize the improved search system"""
        
        # NLP setup
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english')) | {"university", "please", "can"}
        
        # File paths
        self.data_file_path = data_file_path
        self.feedback_file_path = "user_feedback_data.json"
        self.disliked_answers_file = "disliked_answers.json"
        
        # Load and process data
        self.load_data()
        self.load_feedback_data()
        self.preprocess_all_data()
        self.train_models()
        
        print(f"✅ Improved Search System initialized with {len(self.data)} total data points")
        print(f"📊 Available data after filtering: {len(self.questions)}")
        print(f"🚫 Blocked answers: {len(self.disliked_answers)}")
    
    def load_data(self):
        """Load JSON data"""
        try:
            with open(self.data_file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            if not isinstance(self.data, list):
                self.data = []
        except Exception as e:
            print(f"Error loading data: {e}")
            self.data = []
    
    def load_feedback_data(self):
        """Load feedback and disliked answers"""
        # Load disliked answers
        try:
            with open(self.disliked_answers_file, 'r', encoding='utf-8') as f:
                self.disliked_answers = json.load(f)
        except:
            self.disliked_answers = []
        
        # Load general feedback
        try:
            with open(self.feedback_file_path, 'r', encoding='utf-8') as f:
                self.feedback_data = json.load(f)
        except:
            self.feedback_data = []
    
    def save_feedback_data(self):
        """Save feedback data"""
        os.makedirs(os.path.dirname(self.disliked_answers_file) if os.path.dirname(self.disliked_answers_file) else '.', exist_ok=True)
        
        with open(self.disliked_answers_file, "w", encoding='utf-8') as f:
            json.dump(self.disliked_answers, f, indent=2, ensure_ascii=False)
        
        with open(self.feedback_file_path, "w", encoding='utf-8') as f:
            json.dump(self.feedback_data, f, indent=2, ensure_ascii=False)
    
    def preprocess(self, text: str) -> str:
        """Text preprocessing without aggressive keyword blocking"""
        if not text:
            return ""
        
        text = text.lower().strip()
        text = ''.join([c for c in text if c.isalnum() or c.isspace()])
        words = [self.lemmatizer.lemmatize(word) for word in text.split() 
                if word not in self.stop_words]
        return ' '.join(words)
    
    def preprocess_all_data(self):
        """Preprocess data without blocking keywords globally"""
        self.questions = []
        self.answers = []
        self.keywords_list = []
        self.categories = []
        
        for item in self.data:
            # Only skip if this SPECIFIC answer is in disliked list
            if any(disliked['answer'] == item['answer'] for disliked in self.disliked_answers):
                continue
            
            # Process all data normally (don't filter keywords)
            processed_question = self.preprocess(item["question"])
            processed_keywords = [self.preprocess(kw) for kw in item.get("keywords", [])]
            
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
        """Train ML models on available data"""
        if not self.questions:
            print("⚠️ No valid questions after filtering!")
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
        if len(set(encoded_categories)) > 1:
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
        IMPROVED SEARCH WITH NEXT-BEST ANSWER SELECTION
        - Finds multiple candidates
        - Returns best non-blocked answer
        - Prevents keyword over-blocking
        """
        
        if not self.questions:
            return self._fallback_response("No data available", user_input)
        
        processed_input = self.preprocess(user_input)
        
        # Handle special cases
        special_response = self._handle_special_cases(user_input)
        if special_response:
            return special_response
        
        # Vectorize user input
        try:
            user_vec = self.vectorizer.transform([processed_input])
        except Exception:
            return self._fallback_response("Processing error", user_input)
        
        # Category prediction
        predicted_category = "general"
        category_confidence = 0.5
        
        if self.category_classifier:
            try:
                predicted_category_encoded = self.category_classifier.predict(user_vec)[0]
                predicted_category = self.label_encoder.inverse_transform([predicted_category_encoded])[0]
                category_confidence = np.max(self.category_classifier.predict_proba(user_vec))
            except Exception:
                pass
        
        # Calculate similarities
        all_similarities = cosine_similarity(user_vec, self.X).flatten()
        
        # Enhanced scoring
        enhanced_scores = np.zeros(len(self.questions))
        input_words = set(processed_input.split())
        
        for i in range(len(self.questions)):
            base_score = all_similarities[i]
            processed_question = self.questions[i]
            
            # Exact question matching
            exact_bonus = 0.0
            if processed_input == processed_question:
                exact_bonus = 1.0
            elif len(input_words.intersection(set(processed_question.split()))) >= len(input_words) * 0.8:
                exact_bonus = 0.8
            
            # Keyword matching
            item_keywords = set(self.keywords_list[i])
            keyword_matches = len(input_words.intersection(item_keywords))
            keyword_score = keyword_matches / max(len(item_keywords), 1) if item_keywords else 0
            
            # Category bonus
            category_bonus = 0.3 if self.categories[i] == predicted_category else 0.0
            
            # Question word overlap
            question_words = set(processed_question.split())
            question_overlap = len(input_words.intersection(question_words))
            question_bonus = question_overlap / max(len(question_words), 1) if question_words else 0
            
            # Final score calculation
            if exact_bonus > 0.7:
                enhanced_scores[i] = (
                    exact_bonus * 0.6 +
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
        
        # FIND MULTIPLE CANDIDATES AND SELECT BEST NON-BLOCKED
        if len(enhanced_scores) == 0:
            return self._fallback_response("No matches found", user_input)
        
        # Get top 10 candidates
        sorted_indices = np.argsort(enhanced_scores)[::-1]
        top_candidates = sorted_indices[:10]
        
        # Find first non-blocked answer with good score
        for rank, idx in enumerate(top_candidates):
            candidate_answer = self.answers[idx]
            candidate_score = enhanced_scores[idx]
            
            # Check if this specific answer is blocked
            is_blocked = any(disliked['answer'] == candidate_answer for disliked in self.disliked_answers)
            
            if not is_blocked and candidate_score >= threshold:
                final_confidence = candidate_score * (0.7 + category_confidence * 0.3)
                
                return {
                    "answer": candidate_answer,
                    "confidence": float(min(final_confidence, 1.0)),
                    "source": "improved_search",
                    "method": "next_best_selection",
                    "analyzed_items": len(self.questions),
                    "total_original_items": len(self.data),
                    "blocked_answers": len(self.disliked_answers),
                    "predicted_category": str(predicted_category),
                    "category_confidence": float(category_confidence),
                    "base_similarity": float(all_similarities[idx]),
                    "enhanced_score": float(candidate_score),
                    "candidate_rank": rank + 1,
                    "alternatives_checked": len(top_candidates)
                }
        
        # If all good candidates are blocked
        blocked_count = sum(1 for idx in top_candidates 
                          if any(disliked['answer'] == self.answers[idx] 
                                for disliked in self.disliked_answers))
        
        return self._fallback_response("Best matches blocked by feedback", user_input, {
            "blocked_candidates": blocked_count,
            "total_candidates": len(top_candidates),
            "best_score": float(enhanced_scores[sorted_indices[0]])
        })
    
    def _handle_special_cases(self, user_input: str) -> Optional[Dict[str, Any]]:
        """Handle special cases"""
        user_lower = user_input.lower()
        
        if 'time' in user_lower:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return {
                "answer": f"The current time is {now}.",
                "confidence": 1.0,
                "source": "special_command",
                "method": "direct_response"
            }
        
        if any(phrase in user_lower for phrase in ["how are you", "how r u"]):
            return {
                "answer": "I'm doing well, thank you! How can I help you with information about Green University?",
                "confidence": 1.0,
                "source": "greeting",
                "method": "direct_response"
            }
        
        return None
    
    def _fallback_response(self, reason: str, user_input: str, extra_info: Dict = None) -> Dict[str, Any]:
        """Fallback response when no good match found"""
        return {
            "answer": ("I don't have specific information about that. "
                      "You can contact Green University directly at: "
                      "Phone: +880-2-7791071-5, Admission: 01775234234, "
                      "Email: info@green.edu.bd, Website: https://www.green.edu.bd/"),
            "confidence": 0.15,
            "source": "fallback",
            "method": "no_suitable_match",
            "reason": reason,
            "analyzed_items": len(self.questions) if hasattr(self, 'questions') else 0,
            **(extra_info or {})
        }
    
    def record_user_feedback(self, user_question: str, bot_answer: str, feedback_type: str) -> Dict[str, Any]:
        """Record feedback - only block specific answers, not keywords"""
        timestamp = datetime.datetime.now().isoformat()
        
        # Record feedback
        feedback_entry = {
            'timestamp': timestamp,
            'question': user_question,
            'answer': bot_answer,
            'feedback': feedback_type
        }
        self.feedback_data.append(feedback_entry)
        
        # Handle DISLIKE - block only the specific answer
        if feedback_type == 'dislike':
            dislike_entry = {
                'answer': bot_answer,
                'question': user_question,
                'timestamp': timestamp,
                'blocked_permanently': True
            }
            self.disliked_answers.append(dislike_entry)
            
            print(f"🚫 Blocked specific answer: '{bot_answer[:50]}...'")
            print(f"📊 Total blocked answers: {len(self.disliked_answers)}")
            
            # Retrain without this specific answer
            self.preprocess_all_data()
            self.train_models()
            
            # Save feedback
            self.save_feedback_data()
            
            return {
                "status": "success",
                "message": "Specific answer blocked. System will find next best answer for similar questions.",
                "blocked_answers": len(self.disliked_answers),
                "available_data": len(self.questions)
            }
        
        # Handle LIKE
        elif feedback_type == 'like':
            self.save_feedback_data()
            return {
                "status": "success", 
                "message": "Positive feedback recorded"
            }
        
        return {"status": "success", "message": "Feedback recorded"}
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        return {
            "total_original_data": len(self.data),
            "available_data": len(self.questions) if hasattr(self, 'questions') else 0,
            "blocked_answers": len(self.disliked_answers),
            "total_feedback": len(self.feedback_data),
            "likes": len([f for f in self.feedback_data if f.get('feedback') == 'like']),
            "dislikes": len([f for f in self.feedback_data if f.get('feedback') == 'dislike'])
        }

# Global system instance
improved_search_system = None

def initialize_improved_system(data_file: str = "enhanced_ndata.json") -> ImprovedChatbotSearchSystem:
    """Initialize improved search system"""
    global improved_search_system
    improved_search_system = ImprovedChatbotSearchSystem(data_file)
    return improved_search_system

def search_with_improved_learning(user_input: str) -> Dict[str, Any]:
    """Main search function with improved learning"""
    global improved_search_system
    if not improved_search_system:
        improved_search_system = initialize_improved_system()
    
    return improved_search_system.comprehensive_search(user_input)

def record_improved_feedback(user_question: str, bot_answer: str, feedback_type: str) -> Dict[str, Any]:
    """Record feedback with improved system"""
    global improved_search_system
    if not improved_search_system:
        improved_search_system = initialize_improved_system()
    
    return improved_search_system.record_user_feedback(user_question, bot_answer, feedback_type)

def get_improved_stats() -> Dict[str, Any]:
    """Get improved system statistics"""
    global improved_search_system
    if not improved_search_system:
        improved_search_system = initialize_improved_system()
    
    return improved_search_system.get_system_stats()

if __name__ == "__main__":
    # Test the improved system
    system = initialize_improved_system()
    
    print("\n🔍 Testing Improved Search System:")
    
    # Test search
    result = system.comprehensive_search("What is the tuition fee for CSE?")
    print(f"💬 Answer: {result['answer'][:100]}...")
    print(f"🎯 Confidence: {result['confidence']:.2f}")
    print(f"📊 Stats: {system.get_system_stats()}")
