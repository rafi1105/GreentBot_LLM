#!/usr/bin/env python3
"""
Data Summary Tool - Show statistics about the enhanced JSON data
"""

import json
from collections import Counter

def analyze_data(filename):
    """Analyze the enhanced JSON data and show statistics"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return

    print(f"📊 Data Analysis for {filename}")
    print("=" * 60)
    
    # Basic statistics
    print(f"📝 Total Items: {len(data)}")
    
    # Keywords analysis
    all_keywords = []
    for item in data:
        all_keywords.extend(item.get('keywords', []))
    
    print(f"🔤 Total Keywords: {len(all_keywords)}")
    print(f"🔤 Unique Keywords: {len(set(all_keywords))}")
    print(f"📊 Average Keywords per Item: {len(all_keywords) / len(data):.1f}")
    
    # Most common keywords
    keyword_counts = Counter(all_keywords)
    print(f"\n🔥 Top 15 Most Common Keywords:")
    for keyword, count in keyword_counts.most_common(15):
        print(f"   • {keyword}: {count}")
    
    # Categories analysis
    all_categories = []
    for item in data:
        all_categories.extend(item.get('categories', []))
    
    if all_categories:
        category_counts = Counter(all_categories)
        print(f"\n📂 Categories Distribution:")
        for category, count in category_counts.items():
            print(f"   • {category}: {count} items")
    
    # Sample high-confidence items
    if any('confidence_score' in item for item in data):
        high_confidence = [item for item in data if item.get('confidence_score', 0) > 0.7]
        print(f"\n⭐ High Confidence Items: {len(high_confidence)}")
        
        if high_confidence:
            print(f"\n📋 Sample High-Confidence Responses:")
            for i, item in enumerate(high_confidence[:3]):
                print(f"   {i+1}. Q: {item['question'][:80]}...")
                print(f"      Keywords: {len(item.get('keywords', []))}")
                print(f"      Confidence: {item.get('confidence_score', 0):.2f}")
                print()
    
    # Question length analysis
    question_lengths = [len(item['question']) for item in data]
    avg_question_length = sum(question_lengths) / len(question_lengths)
    print(f"📏 Average Question Length: {avg_question_length:.1f} characters")
    
    # Answer length analysis
    answer_lengths = [len(item['answer']) for item in data]
    avg_answer_length = sum(answer_lengths) / len(answer_lengths)
    print(f"📏 Average Answer Length: {avg_answer_length:.1f} characters")
    
    print(f"\n✨ Data Quality Indicators:")
    print(f"   • Items with 10+ keywords: {sum(1 for item in data if len(item.get('keywords', [])) >= 10)}")
    print(f"   • Items with categories: {sum(1 for item in data if item.get('categories'))}")
    print(f"   • Items with question variations: {sum(1 for item in data if item.get('question_variations'))}")

if __name__ == "__main__":
    print("🤖 Green University Chatbot - Data Analysis Tool")
    print("=" * 60)
    
    # Analyze both files
    files_to_analyze = [
        "enhanced_ndata.json",
        "optimized_offline_data.json"
    ]
    
    for filename in files_to_analyze:
        try:
            analyze_data(filename)
            print("\n" + "=" * 60)
        except Exception as e:
            print(f"Could not analyze {filename}: {e}")
    
    print("✅ Analysis complete!")
