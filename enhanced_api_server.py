#!/usr/bin/env python3
"""
Enhanced API Server for Green University Chatbot
- Uses comprehensive search through ALL JSON data
- Handles user feedback and learning
- Permanently removes disliked answers and keywords
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import traceback

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the improved search system (fixed next-best-answer logic)
from improved_search_system import (
    initialize_improved_system, 
    search_with_improved_learning, 
    record_improved_feedback, 
    get_improved_stats
)

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Set default JSON encoder to handle UTF-8
app.config['JSON_AS_ASCII'] = False

# Initialize the improved search system
print("🚀 Initializing Improved Search System...")
try:
    enhanced_system = initialize_improved_system("react-chatbot/enhanced_ndata.json")
    print("✅ Improved Search System ready!")
except Exception as e:
    print(f"❌ Failed to initialize improved system: {e}")
    enhanced_system = None

@app.route('/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint - uses enhanced comprehensive search
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message.strip():
            return jsonify({
                'answer': 'Please provide a question.',
                'confidence': 0.0,
                'method': 'validation_error'
            })
          # Get comprehensive search response
        result = search_with_improved_learning(user_message)
        
        # Log the search result
        print(f"🔍 Search Query: {user_message}")
        print(f"📊 Analyzed: {result.get('analyzed_items', 0)} items")
        print(f"🎯 Confidence: {result.get('confidence', 0):.2f}")
        print(f"🔧 Method: {result.get('method', 'unknown')}")
        
        return jsonify(result)
    
    except Exception as e:
        print(f"❌ Chat endpoint error: {e}")
        traceback.print_exc()
        return jsonify({
            'answer': 'I apologize, but I encountered an error. Please try again.',
            'confidence': 0.0,
            'method': 'error_fallback',
            'error': str(e)
        }), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    """
    Feedback endpoint - records user likes/dislikes and learns from them
    """
    try:
        data = request.get_json()
        user_question = data.get('question', '')
        bot_answer = data.get('answer', '')
        feedback_type = data.get('feedback', '')  # 'like' or 'dislike'
        
        if not all([user_question, bot_answer, feedback_type]):
            return jsonify({'error': 'Missing required fields: question, answer, feedback'}), 400
        
        if feedback_type not in ['like', 'dislike']:
            return jsonify({'error': 'Feedback must be either "like" or "dislike"'}), 400
        
        # Record feedback and handle learning
        result = record_improved_feedback(user_question, bot_answer, feedback_type)
        
        # Log feedback
        print(f"💬 Feedback received: {feedback_type}")
        print(f"📝 Question: {user_question}")
        print(f"💡 Answer: {bot_answer[:50]}...")
        
        if feedback_type == 'dislike':
            print("🚫 Answer permanently blocked from future responses")
            stats = get_improved_stats()
            print(f"📊 System Stats: {stats['blocked_answers']} blocked answers, {stats['total_feedback']} total feedback")
        
        return jsonify(result)
    
    except Exception as e:
        print(f"❌ Feedback endpoint error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/stats', methods=['GET'])
def stats():
    """
    System statistics endpoint - shows search performance and learning data
    """
    try:
        stats = get_improved_stats()
        return jsonify(stats)
    
    except Exception as e:
        print(f"❌ Stats endpoint error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Detailed analysis endpoint - shows how search works
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message.strip():
            return jsonify({'error': 'Message is required'})
        
        # Get comprehensive search result with extra details
        result = search_with_improved_learning(user_message)
        
        # Add analysis details
        stats = get_improved_stats()
        analysis_result = {
            'search_result': result,
            'system_stats': stats,
            'analysis_summary': {
                'total_data_points': stats['total_original_data'],
                'available_after_filtering': stats['available_data'],
                'filtered_out_by_dislikes': stats['total_original_data'] - stats['available_data'],
                'search_method': result.get('method', 'unknown'),
                'confidence_level': 'High' if result.get('confidence', 0) > 0.7 else 'Medium' if result.get('confidence', 0) > 0.4 else 'Low'
            }
        }
        
        return jsonify(analysis_result)
    
    except Exception as e:
        print(f"❌ Analyze endpoint error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset():
    """
    Reset endpoint - clears all feedback data (for testing)
    """
    try:
        global enhanced_system
        
        if enhanced_system:
            result = enhanced_system.reset_all_feedback()
            print("🔄 All feedback data reset")
            return jsonify(result)
        else:
            return jsonify({'error': 'Enhanced system not initialized'}), 500
    
    except Exception as e:
        print(f"❌ Reset endpoint error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint
    """
    try:
        stats = get_improved_stats()
        return jsonify({
            'status': 'healthy',
            'message': 'Enhanced Green University Chatbot API is running',
            'features': [
                'Comprehensive data search (ALL JSON items)',
                'User feedback learning',
                'Permanent answer blocking',
                'Keyword filtering',
                'Advanced ML classification',
                'Real-time system adaptation'
            ],
            'system_stats': stats,
            'search_system': 'Enhanced with learning capabilities'
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("\n🚀 Starting Enhanced Green University Chatbot API Server")
    print("📚 Features:")
    print("   ✅ Searches ALL JSON data comprehensively")
    print("   ✅ Learns from user feedback (likes/dislikes)")
    print("   ✅ Permanently removes disliked answers")
    print("   ✅ Blocks keywords from disliked content")
    print("   ✅ Provides diverse responses based on all data")
    print("   ✅ Real-time system adaptation")    
    try:
        stats = get_improved_stats()
        print("\n📊 Current System Status:")
        print(f"   📋 Total original data: {stats['total_original_data']}")
        print(f"   ✅ Available data: {stats['available_data']}")
        print(f"   🚫 Blocked answers: {stats['disliked_answers']}")
        print(f"   🔒 Blocked keywords: {stats['blocked_keywords']}")
        print(f"   💬 Total feedback: {stats['total_feedback']}")
    except Exception as e:
        print(f"   ⚠️ Could not load system stats: {e}")
    
    print("\n🌐 Server starting on http://localhost:5000")
    print("   📡 Endpoints:")
    print("     POST /chat - Main chat interface")
    print("     POST /feedback - Record user feedback")
    print("     GET /stats - System statistics")
    print("     POST /analyze - Detailed search analysis")
    print("     POST /reset - Reset all feedback data")
    print("     GET /health - Health check")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
