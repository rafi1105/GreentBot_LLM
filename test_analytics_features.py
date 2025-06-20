#!/usr/bin/env python3
"""
Test script to verify the Learning Analytics and Feedback Data Analysis features
"""

import requests
import time
import json

def test_analytics_functionality():
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Learning Analytics and Feedback Data Analysis")
    print("=" * 60)
    
    # Step 1: Get current stats
    print("\n📊 Step 1: Getting current system stats...")
    try:
        stats_response = requests.get(f"{base_url}/stats")
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print(f"✅ Current stats:")
            print(f"   📋 Total feedback: {stats.get('total_feedback', 0)}")
            print(f"   👍 Likes: {stats.get('likes', 0)}")
            print(f"   👎 Dislikes: {stats.get('dislikes', 0)}")
            print(f"   🚫 Blocked answers: {stats.get('blocked_answers', 0)}")
            print(f"   📊 Available data: {stats.get('available_data', 0)}")
        else:
            print(f"❌ Failed to get stats: {stats_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting stats: {e}")
        return False
    
    # Step 2: Add some test feedback if needed
    if stats.get('total_feedback', 0) < 3:
        print(f"\n📝 Step 2: Adding test feedback data...")
        
        test_interactions = [
            {
                "question": "What are the admission requirements?",
                "feedback": "like"
            },
            {
                "question": "How much is the tuition fee?", 
                "feedback": "like"
            },
            {
                "question": "What programs are offered?",
                "feedback": "dislike"
            }
        ]
        
        for interaction in test_interactions:
            try:
                # Get chat response first
                chat_response = requests.post(f"{base_url}/chat", 
                                            json={"message": interaction["question"]})
                if chat_response.status_code == 200:
                    chat_data = chat_response.json()
                    answer = chat_data.get('answer', 'Test answer')
                    
                    # Submit feedback
                    feedback_response = requests.post(f"{base_url}/feedback",
                                                    json={
                                                        "question": interaction["question"],
                                                        "answer": answer,
                                                        "feedback": interaction["feedback"]
                                                    })
                    if feedback_response.status_code == 200:
                        print(f"   ✅ Added {interaction['feedback']} for: {interaction['question'][:50]}...")
                    else:
                        print(f"   ❌ Failed to add feedback: {feedback_response.status_code}")
                
                time.sleep(0.5)  # Small delay between requests
                
            except Exception as e:
                print(f"   ⚠️ Error with test interaction: {e}")
    
    # Step 3: Get updated stats
    print(f"\n📈 Step 3: Getting updated stats...")
    try:
        stats_response = requests.get(f"{base_url}/stats")
        if stats_response.status_code == 200:
            final_stats = stats_response.json()
            print(f"✅ Updated stats:")
            print(f"   📋 Total feedback: {final_stats.get('total_feedback', 0)}")
            print(f"   👍 Likes: {final_stats.get('likes', 0)}")
            print(f"   👎 Dislikes: {final_stats.get('dislikes', 0)}")
            print(f"   🚫 Blocked answers: {final_stats.get('blocked_answers', 0)}")
            
            if final_stats.get('total_feedback', 0) > 0:
                satisfaction = (final_stats.get('likes', 0) / final_stats.get('total_feedback', 1)) * 100
                print(f"   😊 Satisfaction rate: {satisfaction:.1f}%")
            else:
                print(f"   ⚠️ No feedback data available")
        
    except Exception as e:
        print(f"❌ Error getting final stats: {e}")
        return False
    
    print(f"\n✅ Analytics test complete!")
    print(f"\n📋 Instructions:")
    print(f"   1. Open the chatbot: file:///d:/VS Code/GreentBot/react-chatbot/index.html")
    print(f"   2. Click the 📊 button (Learning Statistics) - should show stats panel")
    print(f"   3. Click the 🔍 button (Feedback Analysis) - should show analysis modal")
    print(f"   4. Click the 🧪 test button to run debug test")
    print(f"   5. Check browser console (F12) for debug logs")
    
    return True

if __name__ == "__main__":
    test_analytics_functionality()
