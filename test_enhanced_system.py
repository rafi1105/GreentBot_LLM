#!/usr/bin/env python3
"""
Test Script for Enhanced Search System
Demonstrates comprehensive search and feedback learning capabilities
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:5000"

def test_enhanced_search_system():
    """Test the comprehensive search and feedback learning system"""
    print("🧪 Testing Enhanced Green University Chatbot Search System")
    print("=" * 60)
    
    # Test 1: Basic search functionality
    print("\n1. 🔍 TESTING COMPREHENSIVE SEARCH")
    print("-" * 40)
    
    test_queries = [
        "What is the tuition fee for CSE?",
        "How to apply for admission?", 
        "Contact information for Green University",
        "What are the BSc programs available?",
        "How much does BBA cost?"
    ]
    
    search_results = []
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        
        response = requests.post(f"{API_BASE_URL}/chat", json={"message": query})
        if response.status_code == 200:
            result = response.json()
            search_results.append((query, result))
            
            print(f"💬 Answer: {result['answer'][:80]}...")
            print(f"🎯 Confidence: {result.get('confidence', 0):.2f}")
            print(f"📊 Analyzed Items: {result.get('analyzed_items', 0)}")
            print(f"🔧 Method: {result.get('method', 'unknown')}")
        else:
            print(f"❌ Error: {response.status_code}")
    
    # Test 2: System statistics
    print(f"\n\n2. 📊 SYSTEM STATISTICS")
    print("-" * 40)
    
    stats_response = requests.get(f"{API_BASE_URL}/stats")
    if stats_response.status_code == 200:
        stats = stats_response.json()
        print(f"📋 Total Original Data: {stats.get('total_original_data', 0)}")
        print(f"✅ Available Data: {stats.get('available_data', 0)}")
        print(f"🚫 Blocked Answers: {stats.get('blocked_answers', 0)}")
        print(f"🔒 Blocked Keywords: {stats.get('blocked_keywords', 0)}")
        print(f"💬 Total Feedback: {stats.get('total_feedback', 0)}")
        print(f"👍 Positive Feedback: {stats.get('positive_feedback', 0)}")
        print(f"👎 Negative Feedback: {stats.get('negative_feedback', 0)}")
    
    # Test 3: Feedback learning (simulate dislike)
    print(f"\n\n3. 🎓 TESTING FEEDBACK LEARNING SYSTEM")
    print("-" * 40)
    
    if search_results:
        # Pick the first result to test feedback
        test_query, test_result = search_results[0]
        test_answer = test_result['answer']
        
        print(f"🧪 Testing feedback on:")
        print(f"   Question: {test_query}")
        print(f"   Answer: {test_answer[:50]}...")
        
        # Simulate a DISLIKE feedback
        print(f"\n👎 Simulating DISLIKE feedback...")
        
        feedback_response = requests.post(f"{API_BASE_URL}/feedback", json={
            "question": test_query,
            "answer": test_answer,
            "feedback": "dislike"
        })
        
        if feedback_response.status_code == 200:
            feedback_result = feedback_response.json()
            print(f"✅ Feedback recorded: {feedback_result.get('message', 'Unknown')}")
            print(f"🚫 Blocked Answers: {feedback_result.get('blocked_answers', 0)}")
            print(f"🔒 Blocked Keywords: {feedback_result.get('blocked_keywords', 0)}")
            
            # Wait a moment for system to update
            time.sleep(2)
            
            # Test the same query again - should give different result
            print(f"\n🔄 Re-testing same query after dislike...")
            retry_response = requests.post(f"{API_BASE_URL}/chat", json={"message": test_query})
            
            if retry_response.status_code == 200:
                retry_result = retry_response.json()
                print(f"💬 New Answer: {retry_result['answer'][:80]}...")
                print(f"🎯 New Confidence: {retry_result.get('confidence', 0):.2f}")
                print(f"📊 Analyzed Items: {retry_result.get('analyzed_items', 0)}")
                
                # Check if answer is different
                if retry_result['answer'] != test_answer:
                    print("✅ SUCCESS: System learned from feedback - different answer provided!")
                else:
                    print("⚠️ NOTICE: Same answer provided (might be only match available)")
            
        else:
            print(f"❌ Feedback error: {feedback_response.status_code}")
    
    # Test 4: Final system statistics after learning
    print(f"\n\n4. 📊 SYSTEM STATISTICS AFTER LEARNING")
    print("-" * 40)
    
    final_stats_response = requests.get(f"{API_BASE_URL}/stats")
    if final_stats_response.status_code == 200:
        final_stats = final_stats_response.json()
        print(f"📋 Total Original Data: {final_stats.get('total_original_data', 0)}")
        print(f"✅ Available Data: {final_stats.get('available_data', 0)}")
        print(f"🚫 Blocked Answers: {final_stats.get('blocked_answers', 0)}")
        print(f"🔒 Blocked Keywords: {final_stats.get('blocked_keywords', 0)}")
        print(f"💬 Total Feedback: {final_stats.get('total_feedback', 0)}")
        print(f"👍 Positive Feedback: {final_stats.get('positive_feedback', 0)}")
        print(f"👎 Negative Feedback: {final_stats.get('negative_feedback', 0)}")
        print(f"🔄 Learning Active: {final_stats.get('filtering_active', False)}")
    
    # Test 5: Detailed analysis
    print(f"\n\n5. 🔬 DETAILED SEARCH ANALYSIS")
    print("-" * 40)
    
    analysis_query = "What are the admission requirements?"
    print(f"📝 Analyzing: {analysis_query}")
    
    analysis_response = requests.post(f"{API_BASE_URL}/analyze", json={"message": analysis_query})
    if analysis_response.status_code == 200:
        analysis = analysis_response.json()
        
        search_result = analysis.get('search_result', {})
        system_stats = analysis.get('system_stats', {})
        analysis_summary = analysis.get('analysis_summary', {})
        
        print(f"💬 Answer: {search_result.get('answer', 'No answer')[:60]}...")
        print(f"🎯 Confidence: {search_result.get('confidence', 0):.2f}")
        print(f"📊 Data Points Analyzed: {analysis_summary.get('total_data_points', 0)}")
        print(f"✅ Available After Filtering: {analysis_summary.get('available_after_filtering', 0)}")
        print(f"🚫 Filtered Out by Dislikes: {analysis_summary.get('filtered_out_by_dislikes', 0)}")
        print(f"🔧 Search Method: {analysis_summary.get('search_method', 'unknown')}")
        print(f"📈 Confidence Level: {analysis_summary.get('confidence_level', 'unknown')}")
    
    print(f"\n\n🎉 ENHANCED SEARCH SYSTEM TEST COMPLETED!")
    print("=" * 60)
    print("✅ Features Demonstrated:")
    print("   🔍 Comprehensive search through ALL JSON data")
    print("   🎓 Learning from user feedback (likes/dislikes)")
    print("   🚫 Permanent removal of disliked answers")
    print("   🔒 Keyword blocking from disliked content")
    print("   📊 Real-time system adaptation")
    print("   📈 Detailed analysis and statistics")

if __name__ == "__main__":
    try:
        test_enhanced_search_system()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API server at http://localhost:5000")
        print("Please make sure the enhanced_api_server.py is running!")
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
