#!/usr/bin/env python3
"""
Test the fixed Learning Analytics functionality
"""

import requests
import webbrowser
import time

def test_fixed_analytics():
    print("🧪 Testing Fixed Learning Analytics Features")
    print("=" * 50)
    
    # Get current server stats
    response = requests.get("http://localhost:5000/stats")
    if response.ok:
        stats = response.json()
        print("📊 Current Server Stats:")
        print(f"   Total Feedback: {stats['total_feedback']}")
        print(f"   Likes: {stats['likes']}")
        print(f"   Dislikes: {stats['dislikes']}")
        print(f"   Satisfaction: {(stats['likes']/stats['total_feedback']*100):.1f}%")
        print(f"   Blocked Answers: {stats['blocked_answers']}")
        
        print("\n✅ Expected Results:")
        print(f"   📊 Learning Stats Panel should show: {stats['total_feedback']} total, {stats['likes']} likes, {stats['dislikes']} dislikes")
        print(f"   🔍 Analysis Modal should show: {(stats['likes']/stats['total_feedback']*100):.1f}% satisfaction rate")
        print(f"   🎯 Real-time data updates from server")
        
        print(f"\n🌐 Opening browser to test...")
        print(f"   1. Click 📊 button - should show CURRENT server stats")
        print(f"   2. Click 🔍 button - should show detailed analysis")
        print(f"   3. Data should update in real-time!")
        
        # Open browser
        webbrowser.open("file:///d:/VS Code/GreentBot/react-chatbot/index.html")
        
    else:
        print("❌ Server not accessible")

if __name__ == "__main__":
    test_fixed_analytics()
