// Enhanced offline chatbot with comprehensive JSON data
let ENHANCED_CHATBOT_DATA = [];

// Fallback data in case JSON loading fails
const FALLBACK_ENHANCED_DATA = [
    {
        "question": "What is the tuition fee per semester for the BSc in Computer Science and Engineering program?",
        "answer": "The tuition fee for the BSc in Computer Science and Engineering (CSE) program is BDT 70,000 per semester.",
        "keywords": ["BSc", "CSE", "Computer Science", "bdt", "computer", "cost", "tuition", "fee", "semester"],
        "categories": ["fees_tuition", "programs_courses"]
    },
    {
        "question": "How much is the admission fee for undergraduate programs?",
        "answer": "The admission fee for undergraduate programs is BDT 20,000, which is non-refundable.",
        "keywords": ["admission", "application", "apply", "bdt", "cost", "enroll", "enrollment", "fee", "undergraduate"],
        "categories": ["fees_tuition", "admission", "programs_courses"]
    },
    {
        "question": "What is the total tuition fee for the BBA program?",
        "answer": "The total tuition fee for the Bachelor of Business Administration (BBA) program is BDT 60,000 per semester.",
        "keywords": ["BBA", "Business Administration", "bdt", "business", "cost", "tuition", "fee", "semester"],
        "categories": ["fees_tuition", "programs_courses"]
    },
    {
        "question": "What programs does Green University offer?",
        "answer": "Green University offers programs in Computer Science & Engineering (CSE), Business Administration (BBA), English, Electrical & Electronic Engineering (EEE), Civil Engineering, and various other disciplines at undergraduate and graduate levels.",
        "keywords": ["programs", "courses", "departments", "subjects", "study", "CSE", "BBA", "EEE", "civil", "english", "engineering"],
        "categories": ["programs_courses", "general_info"]
    },
    {
        "question": "Where is Green University located?",
        "answer": "Green University of Bangladesh is located in Narayanganj, near Dhaka, Bangladesh. The full address is 220/D, Begum Rokeya Sarani, Senpara Parbata, Mirpur-10, Dhaka-1216.",
        "keywords": ["location", "address", "where", "campus", "narayanganj", "dhaka", "mirpur", "bangladesh"],
        "categories": ["general_info", "contact"]
    },
    {
        "question": "What are the admission requirements?",
        "answer": "Applicants must have a minimum GPA of 2.5 in both SSC and HSC examinations. If a student has a GPA of 2.0 in either SSC or HSC, the combined GPA must be at least 6.0.",
        "keywords": ["admission", "requirements", "gpa", "ssc", "hsc", "eligibility", "qualification", "minimum"],
        "categories": ["admission", "general_info"]
    },
    {
        "question": "Contact information for Green University",
        "answer": "You can contact Green University at: General Phone: +880-2-7791071-5, Enrollment/Admission: 01775234234, Email: info@green.edu.bd, Website: https://www.green.edu.bd/",
        "keywords": ["contact", "phone", "email", "website", "information", "call", "enrollment", "admission"],
        "categories": ["contact", "general_info"]
    },
    {
        "question": "Library facilities at Green University",
        "answer": "Green University has a modern library with digital resources, books, journals, and research materials. There's also a refundable library caution fee of BDT 2,000.",
        "keywords": ["library", "books", "research", "facilities", "digital", "journals", "resources", "caution", "fee"],
        "categories": ["facilities", "fees_tuition"]
    }
];

// Load the optimized data
async function loadEnhancedData() {
    try {
        const response = await fetch('optimized_offline_data.json');
        const data = await response.json();
        ENHANCED_CHATBOT_DATA = data;
        if (typeof window !== 'undefined') {
            window.ENHANCED_CHATBOT_DATA = ENHANCED_CHATBOT_DATA;
        }
        return true;
    } catch (error) {
        // Silently fail and keep using fallback data
        return false;
    }
}

// Enhanced keyword matching function
function findBestEnhancedMatch(userInput) {
    const input = userInput.toLowerCase().trim();
    
    // Handle greetings
    if (input.match(/^(hi|hello|hey|greetings|good morning|good afternoon|good evening).*$/)) {
        return "Hello! Welcome to Green University of Bangladesh chatbot. How can I help you today?";
    }
    
    // Handle how are you
    if (input.match(/(how are you|how r u|how do you do)/)) {
        return "I'm doing great, thank you! I'm here to help you with any questions about Green University. What would you like to know?";
    }
    
    // Handle time requests
    if (input.includes('time')) {
        const now = new Date().toLocaleString();
        return `The current time is ${now}.`;
    }
    
    // Handle goodbye
    if (input.match(/(bye|goodbye|see you|thanks|thank you)/)) {
        return "Thank you for using Green University chatbot. Have a great day!";
    }
    
    // If enhanced data is available, use it
    if (ENHANCED_CHATBOT_DATA.length > 0) {
        return findMatchInEnhancedData(input);
    } else {
        // Fallback to basic data
        return findMatchInBasicData(input);
    }
}

function findMatchInEnhancedData(input) {
    let bestScore = 0;
    let bestAnswer = null;
    let bestCategory = null;
    
    // Process input for better matching
    const inputWords = input.toLowerCase().split(/\s+/);
    const inputText = input.toLowerCase();
    
    for (const item of ENHANCED_CHATBOT_DATA) {
        let score = 0;
        
        // Score based on keyword matches
        for (const keyword of item.keywords) {
            const keywordLower = keyword.toLowerCase();
            
            // Exact keyword match
            if (inputText.includes(keywordLower)) {
                score += 2;
            }
            
            // Word boundary matches
            for (const word of inputWords) {
                if (word === keywordLower) {
                    score += 3;
                } else if (word.includes(keywordLower) || keywordLower.includes(word)) {
                    score += 1;
                }
            }
        }
        
        // Boost score for question similarity
        const questionWords = item.question.toLowerCase().split(/\s+/);
        for (const word of inputWords) {
            if (questionWords.includes(word) && word.length > 3) {
                score += 1;
            }
        }
        
        // Category-based scoring boost
        if (item.categories) {
            for (const category of item.categories) {
                if (category === 'fees_tuition' && input.match(/(fee|cost|price|tuition|money|payment)/)) {
                    score += 2;
                } else if (category === 'admission' && input.match(/(admission|apply|requirement|gpa|eligibility)/)) {
                    score += 2;
                } else if (category === 'programs_courses' && input.match(/(program|course|degree|cse|bba|engineering)/)) {
                    score += 2;
                } else if (category === 'contact_location' && input.match(/(contact|phone|email|address|location)/)) {
                    score += 2;
                }
            }
        }
        
        // Update best match
        if (score > bestScore) {
            bestScore = score;
            bestAnswer = item.answer;
            bestCategory = item.categories ? item.categories[0] : 'general';
        }
    }
    
    // Return best match if score is good enough
    if (bestScore >= 3) {
        return bestAnswer;
    } else {
        // Generate smart fallback based on detected intent
        return generateSmartFallback(input, bestCategory);
    }
}

function generateSmartFallback(input, category) {
    const inputLower = input.toLowerCase();
    
    // Intent-based responses
    if (inputLower.match(/(fee|cost|price|tuition|money)/)) {
        return "I can help you with fee information! Here are the main fees: CSE program is BDT 70,000 per semester, BBA is BDT 60,000 per semester, and admission fee is BDT 20,000. Would you like specific fee details for any program?";
    }
    
    if (inputLower.match(/(admission|apply|requirement)/)) {
        return "For admission to Green University, you need a minimum GPA of 2.5 in both SSC and HSC examinations. We offer programs in CSE, BBA, EEE, Civil Engineering, and English. Would you like specific admission requirements for any program?";
    }
    
    if (inputLower.match(/(program|course|degree|subject)/)) {
        return "Green University offers undergraduate and graduate programs in Computer Science & Engineering (CSE), Business Administration (BBA), Electrical & Electronic Engineering (EEE), Civil Engineering, and English. Which program interests you?";
    }
    
    if (inputLower.match(/(contact|phone|email|address|location)/)) {
        return "You can contact Green University at: Phone: +880-2-7791071-5, Email: info@green.edu.bd, Website: https://www.green.edu.bd/. Our campus is located in Narayanganj, near Dhaka.";
    }
    
    if (inputLower.match(/(scholarship|financial|aid)/)) {
        return "Green University offers various scholarship programs for meritorious students and those from financially disadvantaged backgrounds. Contact our admission office at +880-2-7791071-5 for detailed scholarship information.";
    }
    
    if (inputLower.match(/(campus|facility|library|lab)/)) {
        return "Green University provides modern facilities including well-equipped classrooms, computer labs, library with digital resources, cafeteria, prayer room, and recreational areas. Our library has a refundable caution fee of BDT 2,000.";
    }
    
    // General fallback
    return "I'd be happy to help you with information about Green University! I can assist with: programs & courses, tuition fees, admission requirements, campus facilities, scholarships, contact information, and more. Could you please be more specific about what you'd like to know?";
}

function findMatchInBasicData(input) {
    // Fallback to basic data (the original simple matching)
    let bestScore = 0;
    let bestAnswer = null;
    
    const basicData = [
        {
            question: "What is Green University?",
            answer: "Green University of Bangladesh is a private university established in 2003, located in Narayanganj. It offers undergraduate and graduate programs in various fields including Computer Science, Business Administration, and Engineering.",
            keywords: ["green", "university", "about", "what", "information", "gub"]
        },
        {
            question: "What is the tuition fee for CSE?",
            answer: "The tuition fee for the BSc in Computer Science and Engineering (CSE) program is BDT 70,000 per semester.",
            keywords: ["tuition", "fee", "cse", "computer", "science", "engineering", "cost", "price"]
        },
        {
            question: "What programs does Green University offer?",
            answer: "Green University offers programs in Computer Science & Engineering (CSE), Business Administration (BBA), English, Electrical & Electronic Engineering (EEE), Civil Engineering, and various other disciplines at undergraduate and graduate levels.",
            keywords: ["programs", "courses", "departments", "subjects", "study", "eee", "civil", "english"]
        }
    ];
    
    for (const item of basicData) {
        let score = 0;
        for (const keyword of item.keywords) {
            if (input.includes(keyword.toLowerCase())) {
                score += 1;
            }
        }
        
        if (score > bestScore) {
            bestScore = score;
            bestAnswer = item.answer;
        }
    }
    
    return bestAnswer || "I don't have specific information about that. Please visit our website for more details: https://www.green.edu.bd/";
}

// Initialize enhanced data immediately with fallback data
ENHANCED_CHATBOT_DATA = FALLBACK_ENHANCED_DATA;
if (typeof window !== 'undefined') {
    window.ENHANCED_CHATBOT_DATA = ENHANCED_CHATBOT_DATA;
}

// Try to load JSON data when DOM is ready, but don't block functionality
document.addEventListener('DOMContentLoaded', function() {
    // Only try to load JSON if we're in an HTTP context
    if (window.location.protocol === 'http:' || window.location.protocol === 'https:') {
        loadEnhancedData();
    }
});

// Export for use in main script
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { findBestEnhancedMatch, loadEnhancedData, ENHANCED_CHATBOT_DATA };
} else {
    // Make it available globally for browser use
    window.findBestOfflineMatch = findBestEnhancedMatch;
    window.ENHANCED_CHATBOT_DATA = ENHANCED_CHATBOT_DATA;
}
