#!/usr/bin/env python3
"""
Enhanced JSON Data Generator for Green University Chatbot
Automatically generates more accurate and comprehensive data
"""

import json
import re
from typing import List, Dict, Set

def load_existing_data(filename: str) -> List[Dict]:
    """Load existing JSON data"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return []

def extract_keywords_from_text(text: str) -> Set[str]:
    """Extract meaningful keywords from text"""
    # Remove common words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
        'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after',
        'above', 'below', 'between', 'among', 'is', 'are', 'was', 'were', 'be', 'been',
        'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
    }
    
    # Extract words (3+ characters) and numbers
    words = re.findall(r'\b\w{3,}\b', text.lower())
    keywords = set()
    
    for word in words:
        if word not in stop_words:
            keywords.add(word)
            
            # Add common variations and abbreviations
            if word in ['computer', 'science', 'engineering']:
                if 'computer' in words and 'science' in words:
                    keywords.add('cse')
                    keywords.add('cs')
            elif word in ['business', 'administration']:
                if 'business' in words and 'administration' in words:
                    keywords.add('bba')
            elif word in ['electrical', 'electronic']:
                keywords.add('eee')
                keywords.add('electrical')
                keywords.add('electronic')
            elif word == 'university':
                keywords.add('univ')
                keywords.add('varsity')
                keywords.add('gub')
            elif word == 'green':
                keywords.add('gub')
            elif word == 'tuition':
                keywords.add('fee')
                keywords.add('cost')
                keywords.add('price')
                keywords.add('payment')
            elif word == 'admission':
                keywords.add('apply')
                keywords.add('application')
                keywords.add('entry')
                keywords.add('enroll')
                keywords.add('enrollment')
    
    return keywords

def generate_question_variations(original_question: str) -> List[str]:
    """Generate variations of questions for better matching"""
    variations = [original_question]
    
    # Convert to lowercase for pattern matching
    q_lower = original_question.lower()
    
    # Add common question starters
    if not any(q_lower.startswith(starter) for starter in ['what', 'how', 'when', 'where', 'why', 'who']):
        variations.extend([
            f"What is {original_question.lower()}?",
            f"Tell me about {original_question.lower()}",
            f"Can you explain {original_question.lower()}?"
        ])
    
    # Add informal variations
    informal_patterns = {
        'what is': ['whats', 'what\'s'],
        'how much': ['how much does it cost', 'cost of', 'price of'],
        'where is': ['where can i find', 'location of'],
        'when is': ['when does', 'what time'],
        'admission': ['admission process', 'how to apply', 'application'],
        'fee': ['fees', 'cost', 'price', 'payment'],
        'requirements': ['criteria', 'conditions', 'qualifications']
    }
    
    for pattern, replacements in informal_patterns.items():
        if pattern in q_lower:
            for replacement in replacements:
                new_q = q_lower.replace(pattern, replacement)
                variations.append(new_q.capitalize())
    
    return list(set(variations))  # Remove duplicates

def enhance_keywords(existing_keywords: List[str], question: str, answer: str) -> List[str]:
    """Enhance existing keywords with auto-generated ones"""
    enhanced = set(existing_keywords)
    
    # Extract from question and answer
    question_keywords = extract_keywords_from_text(question)
    answer_keywords = extract_keywords_from_text(answer)
    
    enhanced.update(question_keywords)
    enhanced.update(answer_keywords)
    
    # Add domain-specific keywords
    domain_keywords = {
        'green university': ['gub', 'green', 'university', 'bangladesh'],
        'computer science': ['cse', 'cs', 'programming', 'software', 'it'],
        'business': ['bba', 'management', 'commerce', 'finance'],
        'engineering': ['eng', 'technical', 'technology'],
        'admission': ['apply', 'application', 'entry', 'enroll'],
        'semester': ['term', 'session', 'academic'],
        'fee': ['cost', 'price', 'payment', 'tuition', 'money'],
        'campus': ['university', 'college', 'facility', 'building'],
        'library': ['books', 'study', 'research', 'digital'],
        'scholarship': ['financial', 'aid', 'support', 'merit']
    }
    
    text_combined = (question + ' ' + answer).lower()
    for domain, keywords in domain_keywords.items():
        if any(word in text_combined for word in domain.split()):
            enhanced.update(keywords)
    
    return sorted(list(enhanced))

def add_context_and_alternatives(item: Dict) -> Dict:
    """Add context and alternative phrasings to improve accuracy"""
    enhanced_item = item.copy()
    
    # Generate question variations
    variations = generate_question_variations(item['question'])
    enhanced_item['question_variations'] = variations
    
    # Enhance keywords
    enhanced_keywords = enhance_keywords(item['keywords'], item['question'], item['answer'])
    enhanced_item['keywords'] = enhanced_keywords
    
    # Add confidence score based on keyword density
    text_length = len(item['question'] + ' ' + item['answer'])
    keyword_density = len(enhanced_keywords) / max(text_length / 10, 1)
    enhanced_item['confidence_score'] = min(keyword_density, 1.0)
    
    # Add category classification
    categories = classify_question(item['question'], item['answer'])
    enhanced_item['categories'] = categories
    
    return enhanced_item

def classify_question(question: str, answer: str) -> List[str]:
    """Classify questions into categories for better organization"""
    text = (question + ' ' + answer).lower()
    categories = []
    
    classification_rules = {
        'fees_tuition': ['fee', 'tuition', 'cost', 'price', 'payment', 'money'],
        'admission': ['admission', 'apply', 'application', 'requirement', 'gpa', 'ssc', 'hsc'],
        'programs_courses': ['program', 'course', 'degree', 'bsc', 'bba', 'cse', 'engineering'],
        'academic_calendar': ['semester', 'calendar', 'schedule', 'exam', 'class', 'registration'],
        'facilities': ['library', 'lab', 'campus', 'facility', 'building', 'classroom'],
        'contact_location': ['contact', 'phone', 'email', 'address', 'location', 'office'],
        'general_info': ['university', 'about', 'history', 'mission', 'vision'],
        'scholarships': ['scholarship', 'financial', 'aid', 'merit', 'support']
    }
    
    for category, keywords in classification_rules.items():
        if any(keyword in text for keyword in keywords):
            categories.append(category)
    
    return categories if categories else ['general']

def generate_enhanced_dataset(input_file: str, output_file: str):
    """Generate enhanced dataset with more accurate responses"""
    print(f"Loading data from {input_file}...")
    original_data = load_existing_data(input_file)
    
    if not original_data:
        print("No data found or error loading file.")
        return
    
    print(f"Processing {len(original_data)} items...")
    enhanced_data = []
    
    for i, item in enumerate(original_data):
        if i % 100 == 0:
            print(f"Processing item {i+1}/{len(original_data)}")
        
        try:
            enhanced_item = add_context_and_alternatives(item)
            enhanced_data.append(enhanced_item)
        except Exception as e:
            print(f"Error processing item {i}: {e}")
            enhanced_data.append(item)  # Keep original if enhancement fails
    
    # Save enhanced data
    print(f"Saving enhanced data to {output_file}...")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(enhanced_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Enhanced dataset saved successfully!")
        print(f"📊 Statistics:")
        print(f"   - Original items: {len(original_data)}")
        print(f"   - Enhanced items: {len(enhanced_data)}")
        
        # Calculate average keywords per item
        avg_keywords = sum(len(item.get('keywords', [])) for item in enhanced_data) / len(enhanced_data)
        print(f"   - Average keywords per item: {avg_keywords:.1f}")
        
        # Show categories distribution
        all_categories = []
        for item in enhanced_data:
            all_categories.extend(item.get('categories', []))
        
        category_counts = {}
        for cat in all_categories:
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        print(f"   - Categories found: {list(category_counts.keys())}")
        
    except Exception as e:
        print(f"❌ Error saving file: {e}")

def create_optimized_offline_data(enhanced_file: str, offline_file: str):
    """Create optimized data for offline chatbot"""
    print(f"Creating optimized offline data...")
    
    enhanced_data = load_existing_data(enhanced_file)
    if not enhanced_data:
        return
    
    # Select best items for offline use (high confidence, diverse categories)
    offline_data = []
    category_counts = {}
    
    # Sort by confidence score (if available)
    sorted_data = sorted(enhanced_data, 
                        key=lambda x: x.get('confidence_score', 0.5), 
                        reverse=True)
    
    for item in sorted_data:
        categories = item.get('categories', ['general'])
        
        # Limit items per category for diversity
        should_include = False
        for cat in categories:
            if category_counts.get(cat, 0) < 20:  # Max 20 items per category
                should_include = True
                category_counts[cat] = category_counts.get(cat, 0) + 1
        
        if should_include and len(offline_data) < 100:  # Limit total items
            # Create simplified version for offline use
            simplified_item = {
                'question': item['question'],
                'answer': item['answer'],
                'keywords': item['keywords'][:10],  # Limit keywords
                'categories': categories
            }
            offline_data.append(simplified_item)
    
    # Save optimized offline data
    try:
        with open(offline_file, 'w', encoding='utf-8') as f:
            json.dump(offline_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Optimized offline data saved to {offline_file}")
        print(f"📊 Offline dataset: {len(offline_data)} items")
    except Exception as e:
        print(f"❌ Error saving offline data: {e}")

if __name__ == "__main__":
    # File paths
    input_file = "../ndata.json"
    enhanced_file = "enhanced_ndata.json"
    offline_file = "optimized_offline_data.json"
    
    print("🚀 Starting Enhanced JSON Data Generation...")
    print("=" * 50)
    
    # Step 1: Generate enhanced dataset
    generate_enhanced_dataset(input_file, enhanced_file)
    
    print("\n" + "=" * 50)
    
    # Step 2: Create optimized offline version
    create_optimized_offline_data(enhanced_file, offline_file)
    
    print("\n✨ Data generation complete!")
    print(f"📁 Files created:")
    print(f"   - {enhanced_file} (Full enhanced dataset)")
    print(f"   - {offline_file} (Optimized for offline chatbot)")
