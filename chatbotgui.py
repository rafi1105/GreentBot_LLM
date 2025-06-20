import json
import numpy as np
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from functools import lru_cache
import datetime
from feedback_system import FeedbackLearningSystem

# Initialize feedback system
feedback_system = FeedbackLearningSystem()

# NLP resources
nltk.download('stopwords')
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english')) | {"university", "please", "can"}

# Load and preprocess dataset
json_file_path = "enhanced_ndata.json"
if not os.path.exists(json_file_path):
    json_file_path = "react-chatbot/enhanced_ndata.json"

with open(json_file_path, "r", encoding='utf-8') as f:
    data = json.load(f)

print(f"Loaded {len(data)} data points for comprehensive analysis")

# Optimized text preprocessing function
def preprocess(text):
    text = text.lower().strip()  # Normalize to lowercase and remove extra spaces
    text = ''.join([c for c in text if c.isalnum() or c.isspace()])  # Remove non-alphanumeric characters
    words = [lemmatizer.lemmatize(word) for word in text.split() if
             word not in stop_words]  # Lemmatization and stopword removal
    return ' '.join(words)

# Preprocess the questions and keywords
questions = [preprocess(item["question"]) for item in data]
answers = [item["answer"] for item in data]
raw_keywords = [item["keywords"] for item in data]
normalized_keywords = [[preprocess(kw) for kw in kw_list] for kw_list in raw_keywords]

# Create categories for supervised learning
categories = []
for item in data:
    if "categories" in item and item["categories"]:
        categories.append(item["categories"][0])  # Use first category
    else:
        # Auto-categorize based on keywords
        keywords = [kw.lower() for kw in item["keywords"]]
        if any(word in keywords for word in ["fee", "tuition", "cost", "price"]):
            categories.append("fees")
        elif any(word in keywords for word in ["admission", "requirement", "apply", "enrollment"]):
            categories.append("admission")
        elif any(word in keywords for word in ["program", "course", "department", "cse", "bba"]):
            categories.append("programs")
        elif any(word in keywords for word in ["contact", "phone", "email", "address"]):
            categories.append("contact")
        else:
            categories.append("general")

# Encode categories for supervised learning
label_encoder = LabelEncoder()
encoded_categories = label_encoder.fit_transform(categories)

# Vectorization using TF-IDF
vectorizer = TfidfVectorizer(ngram_range=(1, 3), max_features=10000, min_df=1, max_df=0.95)
X = vectorizer.fit_transform(questions)

# Train supervised learning model for category prediction
X_train, X_test, y_train, y_test = train_test_split(X, encoded_categories, test_size=0.2, random_state=42)
category_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
category_classifier.fit(X_train, y_train)

print(f"Supervised learning model trained with accuracy: {category_classifier.score(X_test, y_test):.3f}")

# Clustering for additional optimization
silhouette_scores = []
cluster_range = range(2, min(20, len(data) // 10) or 3)
for n in cluster_range:
    kmeans = MiniBatchKMeans(n_clusters=n, random_state=0, batch_size=100)
    labels = kmeans.fit_predict(X)
    score = silhouette_score(X, labels)
    silhouette_scores.append(score)

# Choose the optimal cluster count
optimal_clusters = cluster_range[np.argmax(silhouette_scores)]
kmeans = MiniBatchKMeans(n_clusters=optimal_clusters, random_state=0, batch_size=100)
labels = kmeans.fit_predict(X)

# Map clusters to questions
cluster_to_indices = {i: [] for i in range(optimal_clusters)}
for idx, label in enumerate(labels):
    cluster_to_indices[label].append(idx)


# Enhanced comprehensive matching function with supervised learning
def find_best_match_with_supervised_learning(user_input, threshold=0.25):
    """
    COMPREHENSIVE SUPERVISED LEARNING APPROACH
    - Analyzes ALL JSON data before showing output
    - Uses multiple ML techniques for best match
    - Returns only the highest confidence answer
    """
    # First, check if we have a learned improved response
    improved_response = feedback_system.get_improved_response_suggestion(user_input)
    if improved_response and improved_response["confidence"] > 0.8:
        return {
            "answer": improved_response["suggested_answer"],
            "confidence": improved_response["confidence"],
            "source": "learned_pattern",
            "method": "feedback_learning",
            "analyzed_items": 0
        }
    
    processed_input = preprocess(user_input)
    
    # Special case handlers
    if 'time' in user_input.lower():
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return {
            "answer": f"The real time is {now}.",
            "confidence": 1.0,
            "source": "special_command",
            "method": "direct_match",
            "analyzed_items": 0
        }
    
    if any(phrase in user_input.lower() for phrase in ["how are you", "how r u"]):
        return {
            "answer": "Yes, I am fine. Do you have any question about Green University?",
            "confidence": 1.0,
            "source": "greeting_response",
            "method": "direct_match",
            "analyzed_items": 0
        }
    
    # STEP 1: COMPREHENSIVE DATA ANALYSIS
    user_vec = vectorizer.transform([processed_input])
    
    # STEP 2: SUPERVISED LEARNING - Predict category
    predicted_category_encoded = category_classifier.predict(user_vec)[0]
    predicted_category = label_encoder.inverse_transform([predicted_category_encoded])[0]
    category_confidence = np.max(category_classifier.predict_proba(user_vec))
    
    # STEP 3: ANALYZE ALL DATA POINTS
    all_similarities = cosine_similarity(user_vec, X).flatten()
      # STEP 4: ENHANCED SCORING SYSTEM with exact question matching priority
    enhanced_scores = np.zeros(len(data))
    
    for i in range(len(data)):
        # Base similarity score
        base_score = all_similarities[i]
        
        # PRIORITY: Exact question matching (highest weight)
        exact_question_bonus = 0.0
        processed_question = preprocess(data[i]["question"])
        if processed_input == processed_question:
            exact_question_bonus = 1.0  # Perfect match
        elif len(set(processed_input.split()).intersection(set(processed_question.split()))) >= len(processed_input.split()) * 0.8:
            exact_question_bonus = 0.8  # Near-perfect match
        
        # Category matching bonus
        item_category = categories[i]
        category_bonus = 0.3 if item_category == predicted_category else 0.0
        
        # Keyword matching analysis
        input_words = set(processed_input.split())
        item_keywords = set(normalized_keywords[i])
        
        # Exact keyword matches
        exact_matches = len(input_words.intersection(item_keywords))
        keyword_score = exact_matches / max(len(item_keywords), 1) if len(item_keywords) > 0 else 0
        
        # Partial keyword matches
        partial_score = 0
        for input_word in input_words:
            for keyword in item_keywords:
                if len(input_word) > 3 and len(keyword) > 3:
                    if input_word in keyword or keyword in input_word:
                        partial_score += 0.2
        
        # Question similarity bonus (word overlap)
        question_words = set(preprocess(data[i]["question"]).split())
        question_overlap = len(input_words.intersection(question_words))
        question_bonus = question_overlap / max(len(question_words), 1) if len(question_words) > 0 else 0
        
        # Calculate final enhanced score with EXACT QUESTION PRIORITY
        if exact_question_bonus > 0.7:  # If it's an exact or near-exact question match
            enhanced_scores[i] = (
                exact_question_bonus * 0.6 +  # Exact question match (highest priority)
                base_score * 0.25 +  # TF-IDF similarity
                keyword_score * 0.1 +  # Keyword matching
                category_bonus * 0.05  # Category prediction
            )
        else:  # Regular scoring for non-exact matches
            enhanced_scores[i] = (
                base_score * 0.4 +  # TF-IDF similarity
                category_bonus * 0.2 +  # Category prediction
                keyword_score * 0.25 +  # Keyword matching
                partial_score * 0.1 +  # Partial matches
                question_bonus * 0.05  # Question similarity
            )
    
    # STEP 5: FIND BEST MATCH FROM ALL DATA
    best_idx = np.argmax(enhanced_scores)
    best_score = enhanced_scores[best_idx]
    
    # STEP 6: CONFIDENCE CALCULATION
    # Apply category confidence and pattern learning
    pattern_confidence = feedback_system.get_pattern_confidence(user_input)
    final_confidence = best_score * (0.7 + category_confidence * 0.2 + pattern_confidence * 0.1)
    
    # STEP 7: RETURN BEST MATCH OR ENHANCED FALLBACK
    if final_confidence >= threshold:
        return {
            "answer": answers[best_idx],
            "confidence": final_confidence,
            "source": "comprehensive_ml_analysis",
            "method": "supervised_learning",
            "analyzed_items": len(data),
            "predicted_category": predicted_category,
            "category_confidence": category_confidence,
            "matched_question": data[best_idx]["question"],
            "base_similarity": all_similarities[best_idx],
            "enhanced_score": best_score,
            "top_keywords": data[best_idx]["keywords"][:5]
        }
    else:
        # Enhanced fallback with category-specific guidance
        category_guidance = {
            "fees": "tuition fees, admission costs, and payment information",
            "admission": "admission requirements, application process, and enrollment procedures", 
            "programs": "academic programs, courses, and departments",
            "contact": "contact information, phone numbers, and office locations",
            "general": "general information about Green University"
        }
        
        guidance = category_guidance.get(predicted_category, "general information")
        
        fallback_response = (f"I don't have specific information about that. Based on your question, "
                           f"you might be looking for {guidance}. "
                           f"You can contact Green University directly at: "
                           f"Phone: +880-2-7791071-5, Admission: 01775234234, "
                           f"Email: info@green.edu.bd, Website: https://www.green.edu.bd/")
        
        return {
            "answer": fallback_response,
            "confidence": 0.15,
            "source": "enhanced_fallback",
            "method": "category_guided_fallback",
            "analyzed_items": len(data),
            "predicted_category": predicted_category,
            "category_confidence": category_confidence,
            "best_similarity": all_similarities[best_idx],
            "suggested_category": guidance
        }

# Comprehensive analysis function
def analyze_all_data_matches(user_input, show_top=5):
    """
    Analyze and show how the user input matches against ALL JSON data
    Returns detailed analysis of the comprehensive search
    """
    processed_input = preprocess(user_input)
    user_vec = vectorizer.transform([processed_input])
    
    # Get all similarities
    all_similarities = cosine_similarity(user_vec, X).flatten()
    
    # Predict category
    predicted_category_encoded = category_classifier.predict(user_vec)[0]
    predicted_category = label_encoder.inverse_transform([predicted_category_encoded])[0]
    category_proba = category_classifier.predict_proba(user_vec)[0]
      # Calculate enhanced scores for all items with exact question matching priority
    enhanced_scores = []
    for i in range(len(data)):
        input_words = set(processed_input.split())
        item_keywords = set(normalized_keywords[i])
        keyword_overlap = len(input_words.intersection(item_keywords))
        keyword_score = keyword_overlap / max(len(item_keywords), 1) if len(item_keywords) > 0 else 0
        
        # Check for exact question match
        processed_question = preprocess(data[i]["question"])
        exact_question_bonus = 0.0
        if processed_input == processed_question:
            exact_question_bonus = 1.0  # Perfect match
        elif len(set(processed_input.split()).intersection(set(processed_question.split()))) >= len(processed_input.split()) * 0.8:
            exact_question_bonus = 0.8  # Near-perfect match
        
        category_bonus = 0.3 if categories[i] == predicted_category else 0.0
        
        # Prioritize exact question matches
        if exact_question_bonus > 0.7:
            final_score = exact_question_bonus * 0.7 + all_similarities[i] * 0.2 + keyword_score * 0.1
        else:
            final_score = all_similarities[i] * 0.5 + keyword_score * 0.3 + category_bonus * 0.2
        
        enhanced_scores.append({
            "index": i,
            "question": data[i]["question"],
            "answer": data[i]["answer"][:100] + "..." if len(data[i]["answer"]) > 100 else data[i]["answer"],
            "similarity": float(all_similarities[i]),
            "keyword_score": float(keyword_score),
            "exact_question_match": exact_question_bonus > 0.7,
            "exact_question_bonus": float(exact_question_bonus),
            "category": categories[i],
            "category_match": categories[i] == predicted_category,
            "enhanced_score": float(final_score),
            "keywords": data[i]["keywords"][:3]
        })
    
    # Sort by enhanced score
    enhanced_scores.sort(key=lambda x: x["enhanced_score"], reverse=True)
    
    return {
        "user_input": user_input,
        "processed_input": processed_input,
        "predicted_category": predicted_category,
        "category_confidence": float(np.max(category_proba)),
        "total_data_analyzed": len(data),
        "top_matches": enhanced_scores[:show_top],
        "category_distribution": {cat: category_proba[i] for i, cat in enumerate(label_encoder.classes_)},
        "best_match": enhanced_scores[0] if enhanced_scores else None
    }

# Performance monitoring
def get_ml_system_stats():
    """
    Get comprehensive statistics about the ML system
    """
    return {
        "total_data_points": len(data),
        "categories": list(label_encoder.classes_),
        "category_distribution": {cat: categories.count(cat) for cat in set(categories)},
        "vectorizer_features": X.shape[1],
        "supervised_model_accuracy": category_classifier.score(X_test, y_test),
        "clustering_enabled": True,
        "optimal_clusters": optimal_clusters,
        "analysis_method": "comprehensive_supervised_learning"
    }

# Update the main function to use supervised learning
def find_best_match_with_feedback(user_input, threshold=0.25, keyword_boost=0.15):
    """
    Enhanced wrapper that uses comprehensive supervised learning
    """
    return find_best_match_with_supervised_learning(user_input, threshold)

# Backward compatibility - keep original function
@lru_cache(maxsize=500)
def find_best_match(user_input, threshold=0.3, keyword_boost=0.15):
    """Original function for backward compatibility"""
    result = find_best_match_with_feedback(user_input, threshold, keyword_boost)
    return result["answer"]

# Function to record user feedback
def record_user_feedback(user_question, bot_answer, feedback_type, session_id=None):
    """
    Record user feedback for learning
    feedback_type: 'like' or 'dislike'
    """
    try:
        result = feedback_system.record_feedback(user_question, bot_answer, feedback_type, session_id)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Function to get feedback statistics
def get_chatbot_stats():
    """Get comprehensive chatbot performance statistics"""
    try:
        stats = feedback_system.get_feedback_stats()
        return stats
    except Exception as e:
        return {"error": str(e)}


# Test the comprehensive supervised learning system
if __name__ == '__main__':
    print("=" * 70)
    print("🤖 GREEN UNIVERSITY CHATBOT - COMPREHENSIVE SUPERVISED LEARNING SYSTEM")
    print("=" * 70)
      # Display ML system statistics
    ml_stats = get_ml_system_stats()
    print("📊 SYSTEM STATISTICS:")
    print(f"   • Total Data Points Analyzed: {ml_stats['total_data_points']}")
    print(f"   • Categories Detected: {len(ml_stats['categories'])}")
    print(f"   • Supervised Model Accuracy: {ml_stats['supervised_model_accuracy']:.3f}")
    print(f"   • Vectorizer Features: {ml_stats['vectorizer_features']}")
    print(f"   • Analysis Method: {ml_stats['analysis_method'].replace('_', ' ').title()}")
    
    print("\n📂 CATEGORY DISTRIBUTION:")
    for cat, count in ml_stats['category_distribution'].items():
        print(f"   • {cat.title()}: {count} items")
    
    print("\n" + "=" * 70)
    print("🧪 TESTING COMPREHENSIVE DATA ANALYSIS")
    print("=" * 70)
    
    # Test questions to demonstrate comprehensive analysis
    test_questions = [
        "What is the CSE tuition fee?",
        "How can I apply for admission?", 
        "What programs are available?",
        "Contact information for Green University",
        "What are the library facilities?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n🔍 TEST {i}: {question}")
        print("-" * 50)
          # Get comprehensive analysis
        analysis = analyze_all_data_matches(question, show_top=3)
        result = find_best_match_with_supervised_learning(question)
        
        print("📈 ANALYSIS RESULTS:")
        print(f"   • Predicted Category: {analysis['predicted_category'].title()}")
        print(f"   • Category Confidence: {analysis['category_confidence']:.3f}")
        print(f"   • Data Points Analyzed: {analysis['total_data_analyzed']}")
        print(f"   • Final Confidence: {result['confidence']:.3f}")
        print(f"   • Method Used: {result['method'].replace('_', ' ').title()}")
        
        print("\n💡 BEST ANSWER:")
        print(f"   {result['answer'][:150]}{'...' if len(result['answer']) > 150 else ''}")
        
        if 'top_keywords' in result:
            print(f"\n🏷️  MATCHED KEYWORDS: {', '.join(result['top_keywords'])}")
    
    print("\n" + "=" * 70)
    print("✅ COMPREHENSIVE SUPERVISED LEARNING SYSTEM READY!")
    print("🌐 Web interface: http://127.0.0.1:5500/react-chatbot/index.html")
    print("=" * 70)
