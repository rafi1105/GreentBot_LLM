#!/usr/bin/env python3
"""
Flask API Server for Green University Chatbot
Connects comprehensive supervised learning system with JavaScript frontend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the enhanced chatbot
from chatbotgui import find_best_match_with_supervised_learning, analyze_all_data_matches, get_ml_system_stats

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Set default JSON encoder to handle UTF-8
app.config['JSON_AS_ASCII'] = False

@app.route('/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint - uses comprehensive supervised learning
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
        
        # Get comprehensive ML response
        result = find_best_match_with_supervised_learning(user_message)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'answer': 'I apologize, but I encountered an error. Please try again.',
            'confidence': 0.0,
            'method': 'error_fallback',
            'error': str(e)
        }), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Detailed analysis endpoint - shows how input matches against all data
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        show_top = data.get('show_top', 5)
        
        if not user_message.strip():
            return jsonify({'error': 'Message is required'})
        
        # Get comprehensive analysis
        analysis = analyze_all_data_matches(user_message, show_top=show_top)
        
        return jsonify(analysis)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats', methods=['GET'])
def stats():
    """
    System statistics endpoint
    """
    try:
        stats = get_ml_system_stats()
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'message': 'Green University Chatbot API is running',
        'features': [
            'Comprehensive data analysis',
            'Supervised learning',
            'Category prediction',
            'Enhanced keyword matching'
        ]
    })

@app.route('/', methods=['GET'])
def home():
    """
    API documentation endpoint
    """
    return jsonify({
        'name': 'Green University Chatbot API',
        'version': '2.0',
        'description': 'Comprehensive supervised learning chatbot system',
        'endpoints': {
            '/chat': 'POST - Main chat interface',
            '/analyze': 'POST - Detailed analysis of user input',
            '/stats': 'GET - System statistics',
            '/health': 'GET - Health check'
        },
        'features': [
            'Analyzes ALL JSON data before responding',
            'Uses supervised learning for category prediction',
            'Enhanced keyword and semantic matching',
            'Confidence scoring and detailed analytics'
        ]
    })

if __name__ == '__main__':
    print("🚀 Starting Green University Chatbot API Server...")
    print("=" * 60)
    
    # Test the ML system
    try:
        stats = get_ml_system_stats()
        print("✅ ML System Loaded Successfully!")
        print(f"📊 Data Points: {stats['total_data_points']}")
        print(f"🎯 Model Accuracy: {stats['supervised_model_accuracy']:.3f}")
        print(f"📂 Categories: {len(stats['categories'])}")
    except Exception as e:
        print(f"❌ Error loading ML system: {e}")
        sys.exit(1)
    
    print("=" * 60)
    print("🌐 API Server running at: http://localhost:5000")
    print("📖 API Documentation: http://localhost:5000")
    print("💓 Health Check: http://localhost:5000/health")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
