// Enhanced offline chatbot data (extracted from ndata.json)
const CHATBOT_DATA = [
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
        question: "What is the admission fee?",
        answer: "The admission fee for undergraduate programs is BDT 20,000, which is non-refundable.",
        keywords: ["admission", "fee", "undergraduate", "cost", "apply"]
    },
    {
        question: "What is the BBA tuition fee?",
        answer: "The total tuition fee for the Bachelor of Business Administration (BBA) program is BDT 60,000 per semester.",
        keywords: ["bba", "business", "administration", "tuition", "fee"]
    },
    {
        question: "What are additional fees?",
        answer: "Additional fees include an admission form fee of BDT 1,000, ID card and other fees totaling BDT 1,000, EAP 009 course fee of BDT 2,500, PSD 400 course fee of BDT 2,000, and a refundable library caution fee of BDT 2,000.",
        keywords: ["additional", "fees", "id", "card", "library", "eap", "psd"]
    },
    {
        question: "What programs does Green University offer?",
        answer: "Green University offers programs in Computer Science & Engineering (CSE), Business Administration (BBA), English, Electrical & Electronic Engineering (EEE), Civil Engineering, and various other disciplines at undergraduate and graduate levels.",
        keywords: ["programs", "courses", "departments", "subjects", "study", "eee", "civil", "english"]
    },
    {
        question: "Where is Green University located?",
        answer: "Green University of Bangladesh is located in Narayanganj, near Dhaka, Bangladesh. The full address is 220/D, Begum Rokeya Sarani, Senpara Parbata, Mirpur-10, Dhaka-1216.",
        keywords: ["location", "address", "where", "campus", "narayanganj", "dhaka", "mirpur"]
    },
    {
        question: "What are the admission requirements?",
        answer: "Applicants must have a minimum GPA of 2.5 in both SSC and HSC examinations. If a student has a GPA of 2.0 in either SSC or HSC, the combined GPA must be at least 6.0.",
        keywords: ["admission", "requirements", "gpa", "ssc", "hsc", "eligibility", "qualification"]
    },    {
        question: "Contact information for Green University",
        answer: "You can contact Green University at: General Phone: +880-2-7791071-5, Enrollment/Admission: 01775234234, Email: info@green.edu.bd, Website: https://www.green.edu.bd/",
        keywords: ["contact", "phone", "email", "website", "information", "call"]
    },
    {
        question: "Library facilities",
        answer: "Green University has a modern library with digital resources, books, journals, and research materials. There's also a refundable library caution fee of BDT 2,000.",
        keywords: ["library", "books", "research", "facilities", "digital"]
    },
    {
        question: "Semester system",
        answer: "Green University follows a semester system with two main semesters per year (Spring and Fall) and a summer semester. Each semester is typically 15-16 weeks long.",
        keywords: ["semester", "system", "spring", "fall", "summer", "academic"]
    },
    {
        question: "Faculty information",
        answer: "Green University has qualified faculty members with advanced degrees from reputable institutions. The university maintains a good student-to-faculty ratio for quality education.",
        keywords: ["faculty", "teachers", "professors", "staff", "qualified"]
    },
    {
        question: "Campus facilities",
        answer: "Green University provides modern facilities including well-equipped classrooms, computer labs, library, cafeteria, prayer room, and recreational areas for students.",
        keywords: ["campus", "facilities", "labs", "classroom", "cafeteria", "prayer"]
    },
    {
        question: "Scholarships",
        answer: "Green University offers various scholarship programs for meritorious students and those from financially disadvantaged backgrounds. Contact the admission office for detailed information.",
        keywords: ["scholarship", "financial", "aid", "merit", "support", "discount"]
    },
    {
        question: "Online classes",
        answer: "Green University has adapted to online learning systems and offers both in-person and online classes depending on the situation and course requirements.",
        keywords: ["online", "classes", "virtual", "remote", "digital", "elearning"]
    },
    {
        question: "How to enroll or get admission in Green University?",
        answer: "For enrollment and admission to Green University of Bangladesh, please contact us at: Phone: 01775234234 or visit our official website: https://www.green.edu.bd/ for complete admission guidelines and online application process.",
        keywords: ["enroll", "enrollment", "admit", "admission", "apply", "application", "contact", "join", "student", "new", "entry"]
    },
    {
        question: "Enrollment contact number",
        answer: "For enrollment and admission inquiries, please call: 01775234234 or visit our website: https://www.green.edu.bd/ for detailed information and application procedures.",
        keywords: ["enroll", "enrollment", "contact", "number", "phone", "call", "admission", "apply"]
    }
];

// Simple keyword matching function
function findBestOfflineMatch(userInput) {
    const input = userInput.toLowerCase().trim();
    
    // Handle greetings
    if (input.match(/^(hi|hello|hey|greetings).*$/)) {
        return "Hello! Welcome to Green University of Bangladesh chatbot. How can I help you today?";
    }
    
    // Handle how are you
    if (input.match(/(how are you|how r u)/)) {
        return "Yes, I am fine. Do you have any question about Green University?";
    }
    
    // Handle time requests
    if (input.includes('time')) {
        const now = new Date().toLocaleString();
        return `The current time is ${now}.`;
    }
    
    // Handle goodbye
    if (input.match(/(bye|goodbye|see you|thanks)/)) {
        return "Thank you for using Green University chatbot. Have a great day!";
    }
    
    // Find best match based on keywords
    let bestScore = 0;
    let bestAnswer = null;
    
    for (const item of CHATBOT_DATA) {
        let score = 0;
        for (const keyword of item.keywords) {
            if (input.includes(keyword.toLowerCase())) {
                score += 1;
            }
        }
        
        // Boost score if question words match
        const questionWords = item.question.toLowerCase().split(' ');
        for (const word of questionWords) {
            if (input.includes(word) && word.length > 3) {
                score += 0.5;
            }
        }
        
        if (score > bestScore) {
            bestScore = score;
            bestAnswer = item.answer;
        }
    }
    
    // Return best match or fallback
    if (bestScore > 0) {
        return bestAnswer;    } else {
        return "I don't have specific information about that. Here are some topics I can help with: programs & courses, tuition fees, admission requirements, campus facilities, scholarships, contact information, or general questions about Green University. You can also visit our website: https://www.green.edu.bd/";
    }
}

// Export for use in main script
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { findBestOfflineMatch, CHATBOT_DATA };
}

// Make CHATBOT_DATA globally accessible for feedback system
if (typeof window !== 'undefined') {
    window.CHATBOT_DATA = CHATBOT_DATA;
}
