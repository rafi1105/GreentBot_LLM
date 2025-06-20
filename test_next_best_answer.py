#!/usr/bin/env python3
"""
Test script to verify the next-best-answer functionality
"""

import requests
import json

# Test the next-best-answer functionality
def test_next_best_answer():
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Next-Best-Answer Functionality")
    print("=" * 50)
    
    # Test with a common question that might have blocked answers
    test_questions = [
        "What is the tuition fee?",
        "How to apply for admission?", 
        "What programs are available?",
        "Contact information?",
        "CSE department details?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n🔍 Test {i}: '{question}'")
        
        try:
            # Send chat request
            response = requests.post(f"{base_url}/chat", 
                                   json={"message": question},
                                   timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"✅ Answer received:")
                print(f"   📝 Response: {result.get('answer', 'No answer')[:100]}...")
                print(f"   🎯 Confidence: {result.get('confidence', 0):.3f}")
                print(f"   🔧 Method: {result.get('method', 'unknown')}")
                print(f"   📊 Analyzed items: {result.get('analyzed_items', 0)}")
                
                if result.get('method') == 'next_best_selection':
                    print(f"   🎉 SUCCESS: Found next best answer (rank {result.get('candidate_rank', '?')})")
                    print(f"   🔍 Checked {result.get('alternatives_checked', 0)} alternatives")
                elif result.get('method') == 'fallback_response':
                    print(f"   ⚠️ FALLBACK: Using generic response")
                    if 'blocked_candidates' in result:
                        print(f"   🚫 {result['blocked_candidates']} candidates were blocked")
                else:
                    print(f"   ℹ️ Regular match found")
                    
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
    
    print(f"\n📊 Getting final system statistics...")
    try:
        stats_response = requests.get(f"{base_url}/stats")
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print(f"   📋 Total data: {stats.get('total_original_data', 0)}")
            print(f"   ✅ Available: {stats.get('available_data', 0)}")
            print(f"   🚫 Blocked: {stats.get('blocked_answers', 0)}")
            print(f"   💬 Total feedback: {stats.get('total_feedback', 0)}")
    except Exception as e:
        print(f"   ⚠️ Could not get stats: {e}")

if __name__ == "__main__":
    test_next_best_answer()
