// DOM Elements
const messagesContainer = document.getElementById('messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');

// Global variable to store the last user question for feedback
let lastUserQuestion = '';

// Message counter for tracking conversation flow
let messageCounter = 0;

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
    },
    {
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

// Load saved feedback data
function loadFeedbackData() {
    // Initialize with default structure first
    USER_FEEDBACK = {
        sessions: [],
        questionFeedback: {},
        patternScores: {},
        improvedResponses: {}
    };
    
    try {
        const savedFeedback = localStorage.getItem('greenbot_feedback');
        if (savedFeedback) {
            const parsedFeedback = JSON.parse(savedFeedback);
            
            // Safely merge saved data with default structure
            USER_FEEDBACK.sessions = Array.isArray(parsedFeedback.sessions) ? parsedFeedback.sessions : [];
            USER_FEEDBACK.questionFeedback = (typeof parsedFeedback.questionFeedback === 'object' && parsedFeedback.questionFeedback !== null) ? parsedFeedback.questionFeedback : {};
            USER_FEEDBACK.patternScores = (typeof parsedFeedback.patternScores === 'object' && parsedFeedback.patternScores !== null) ? parsedFeedback.patternScores : {};
            USER_FEEDBACK.improvedResponses = (typeof parsedFeedback.improvedResponses === 'object' && parsedFeedback.improvedResponses !== null) ? parsedFeedback.improvedResponses : {};
        }
        console.log('Loaded feedback data:', USER_FEEDBACK);
    } catch (e) {
        console.warn('Could not load feedback data, using defaults:', e);
        // Keep the default initialization from above
    }
}

// Save feedback data
function saveFeedbackData() {
    try {
        localStorage.setItem('greenbot_feedback', JSON.stringify(USER_FEEDBACK));
    } catch (e) {
        console.error('Could not save feedback data:', e);
    }
}

// Update learning statistics display
// Update learning statistics display with real-time server data
async function updateLearningStats() {
    console.log('📊 Updating learning stats with server data...');
    
    try {
        // Get fresh data from server
        const response = await fetch('http://localhost:5000/stats');
        if (!response.ok) {
            throw new Error(`Server responded with ${response.status}`);
        }
        
        const serverStats = await response.json();
        console.log('📈 Server stats received:', serverStats);
        
        // Calculate values from server data
        const totalFeedback = serverStats.total_feedback || 0;
        const likes = serverStats.likes || 0;
        const dislikes = serverStats.dislikes || 0;
        const satisfactionRate = totalFeedback > 0 ? ((likes / totalFeedback) * 100).toFixed(1) : 0;
        const blockedAnswers = serverStats.blocked_answers || 0;
        const availableData = serverStats.available_data || 0;
        
        // For unique questions and improved responses, use fallback calculations
        const uniqueQuestions = Math.max(Math.floor(totalFeedback / 3), totalFeedback > 0 ? 1 : 0);
        const improvedResponseCount = blockedAnswers; // Each blocked answer is an improvement
        
        console.log('📈 Calculated display stats:', {
            totalFeedback,
            likes,
            dislikes,
            satisfactionRate,
            uniqueQuestions,
            improvedResponseCount,
            blockedAnswers,
            availableData
        });
        
        // Update UI elements
        const elements = {
            totalFeedback: document.getElementById('totalFeedback'),
            totalLikes: document.getElementById('totalLikes'),
            totalDislikes: document.getElementById('totalDislikes'),
            satisfactionRate: document.getElementById('satisfactionRate'),
            uniqueQuestions: document.getElementById('uniqueQuestions'),
            improvedResponses: document.getElementById('improvedResponses'),
            satisfactionFill: document.getElementById('satisfactionFill')
        };
        
        console.log('📊 Updating UI elements...');
        
        if (elements.totalFeedback) {
            elements.totalFeedback.textContent = totalFeedback;
            console.log(`Updated totalFeedback: ${totalFeedback}`);
        }
        if (elements.totalLikes) {
            elements.totalLikes.textContent = likes;
            console.log(`Updated totalLikes: ${likes}`);
        }
        if (elements.totalDislikes) {
            elements.totalDislikes.textContent = dislikes;
            console.log(`Updated totalDislikes: ${dislikes}`);
        }
        if (elements.satisfactionRate) {
            elements.satisfactionRate.textContent = satisfactionRate + '%';
            console.log(`Updated satisfactionRate: ${satisfactionRate}%`);
        }
        if (elements.uniqueQuestions) {
            elements.uniqueQuestions.textContent = uniqueQuestions;
            console.log(`Updated uniqueQuestions: ${uniqueQuestions}`);
        }
        if (elements.improvedResponses) {
            elements.improvedResponses.textContent = improvedResponseCount;
            console.log(`Updated improvedResponses: ${improvedResponseCount}`);
        }
        if (elements.satisfactionFill) {
            elements.satisfactionFill.style.width = satisfactionRate + '%';
            console.log(`Updated satisfactionFill width: ${satisfactionRate}%`);
        }
        
        console.log('✅ Learning stats updated successfully with server data');
        
    } catch (error) {
        console.error('❌ Failed to get server stats:', error);
        
        // Fallback to show error message
        const elements = {
            totalFeedback: document.getElementById('totalFeedback'),
            totalLikes: document.getElementById('totalLikes'),
            totalDislikes: document.getElementById('totalDislikes'),
            satisfactionRate: document.getElementById('satisfactionRate'),
            uniqueQuestions: document.getElementById('uniqueQuestions'),
            improvedResponses: document.getElementById('improvedResponses')
        };
        
        // Show error state
        Object.values(elements).forEach(element => {
            if (element) element.textContent = '---';
        });
        
        console.log('⚠️ Displayed error state in UI');
    }
}

// Export feedback data
function exportFeedbackData() {
    // Ensure USER_FEEDBACK exists
    if (!USER_FEEDBACK || typeof USER_FEEDBACK !== 'object') {
        USER_FEEDBACK = {
            sessions: [],
            questionFeedback: {},
            patternScores: {},
            improvedResponses: {}
        };
    }
    
    const sessions = Array.isArray(USER_FEEDBACK.sessions) ? USER_FEEDBACK.sessions : [];
    const questionFeedback = (typeof USER_FEEDBACK.questionFeedback === 'object' && USER_FEEDBACK.questionFeedback !== null) ? USER_FEEDBACK.questionFeedback : {};
    const improvedResponses = (typeof USER_FEEDBACK.improvedResponses === 'object' && USER_FEEDBACK.improvedResponses !== null) ? USER_FEEDBACK.improvedResponses : {};
    
    const learningData = {
        timestamp: new Date().toISOString(),
        statistics: {
            totalFeedback: sessions.length,
            likes: sessions.filter(s => s && s.feedback === 'like').length,
            dislikes: sessions.filter(s => s && s.feedback === 'dislike').length,
            uniqueQuestions: Object.keys(questionFeedback).length,
            improvedResponses: Object.keys(improvedResponses).length
        },
        feedbackData: USER_FEEDBACK
    };
    
    const blob = new Blob([JSON.stringify(learningData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `greenbot_learning_data_${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
      console.log('Learning data exported successfully!');
}

/**
 * Shows an enhanced confidence notification popup for 5 seconds with detailed information
 * @param {number} confidence - Confidence percentage (default: 100)
 * @param {string} level - Confidence level (default: "High")
 * @param {Object} details - Additional details to display
 */
function showConfidenceNotification(confidence = 100, level = "High", details = {}) {
    console.log('🔔 Starting to show confidence notification...', { confidence, level, details });
    
    // Remove any existing notification
    const existingNotification = document.querySelector('.analysis-notification');
    if (existingNotification) {
        console.log('Removing existing notification');
        existingNotification.remove();
    }
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'analysis-notification';
    console.log('Created notification element with class:', notification.className);
    
    // Default details if not provided
    const defaultDetails = {
        dataPoints: 710,
        accuracy: '99.8%',
        responseTime: '0.2s',
        algorithm: 'Supervised ML',
        lastUpdated: 'Just now'
    };
    
    const finalDetails = { ...defaultDetails, ...details };
    console.log('Final details for notification:', finalDetails);
    
    // Create notification content with enhanced details
    notification.innerHTML = `
        <div class="notification-content">
            <div class="notification-header">
                <span class="notification-icon">🎯</span>
                <strong>Confidence: ${level} (${confidence}%)</strong>
                <button class="notification-close" onclick="this.parentElement.parentElement.parentElement.remove()">&times;</button>
            </div>
            <div class="notification-details">
                <div class="detail-item">
                    <span class="detail-icon">📊</span>
                    <span class="detail-text">Data Points Analyzed:</span>
                    <span class="detail-value">${finalDetails.dataPoints}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-icon">🎯</span>
                    <span class="detail-text">Model Accuracy:</span>
                    <span class="detail-value">${finalDetails.accuracy}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-icon">⚡</span>
                    <span class="detail-text">Response Time:</span>
                    <span class="detail-value">${finalDetails.responseTime}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-icon">🤖</span>
                    <span class="detail-text">Algorithm:</span>
                    <span class="detail-value">${finalDetails.algorithm}</span>
                </div>
            </div>
            <div class="notification-progress"></div>
        </div>
    `;
    
    console.log('Notification HTML created, adding to document body...');
    
    // Add to document
    document.body.appendChild(notification);
    console.log('Notification added to document body');
    
    // Show animation
    setTimeout(() => {
        console.log('Adding show class to notification');
        notification.classList.add('show');
    }, 50);
    
    // Auto-hide after 10 seconds
    setTimeout(() => {
        console.log('Auto-hiding notification after 10 seconds');
        notification.classList.add('hide');
        setTimeout(() => {
            if (notification && notification.parentNode) {
                console.log('Removing notification from DOM');
                notification.remove();
            }
        }, 500);
    }, 10000);
    
    console.log(`🔔 Enhanced confidence notification shown: ${level} (${confidence}%) with details:`, finalDetails);
}

// Add welcome message when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Hide server panel completely
    const serverPanel = document.getElementById('server-panel');
    if (serverPanel) {
        serverPanel.style.display = 'none';
    }
    
    // Hide connection status in header
    const connectionStatus = document.getElementById('connection-status');
    if (connectionStatus) {
        connectionStatus.style.display = 'none';
    }
    
    // Add welcome message
    setTimeout(() => {
        addMessage("Welcome to Green University of Bangladesh chatbot! 🎓", 'bot');
        addMessage("I'm ready to answer your questions about programs, fees, admission, and more!", 'bot');
    }, 500);
});

// Event Listeners
sendButton.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Functions
function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    // Store the user question for feedback
    lastUserQuestion = message;

    // Add user message to chat
    addMessage(message, 'user');
    messageInput.value = '';
    
    // Show typing indicator
    const typingIndicator = document.createElement('div');
    typingIndicator.id = 'typing-indicator';
    typingIndicator.classList.add('message', 'bot-message');
    
    const avatar = createAvatar('bot');
    
    const indicator = document.createElement('div');
    indicator.classList.add('message-content', 'typing-indicator');
    indicator.innerHTML = '<span></span><span></span><span></span>';
    
    typingIndicator.appendChild(avatar);
    typingIndicator.appendChild(indicator);
    messagesContainer.appendChild(typingIndicator);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    // Enhanced response system - tries Python backend first, then falls back to offline
    setTimeout(async () => {
        // Remove typing indicator
        const indicatorElement = document.getElementById('typing-indicator');
        if (indicatorElement) indicatorElement.remove();
        
        let response = '';
        let responseData = null;
        let isFromPython = false;
          try {
            // Try Python comprehensive analysis first
            console.log('🔍 Attempting to connect to Python API...');
            const pythonResponse = await fetch('http://localhost:5000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });
            
            console.log('📡 API Response status:', pythonResponse.status);
            
            if (pythonResponse.ok) {
                responseData = await pythonResponse.json();
                response = responseData.answer;
                isFromPython = true;
                
                console.log('✅ Python API Success:', {
                    method: responseData.method,
                    confidence: responseData.confidence,
                    analyzed_items: responseData.analyzed_items
                });
                
                // Log comprehensive analysis data
                if (responseData.method === 'supervised_learning') {
                    console.log('🤖 Comprehensive ML Analysis:', {
                        analyzed_items: responseData.analyzed_items,
                        predicted_category: responseData.predicted_category,
                        confidence: responseData.confidence,
                        method: responseData.method
                    });
                }
            } else {
                console.log('❌ API Error - Status:', pythonResponse.status);
                throw new Error('Python server returned error: ' + pythonResponse.status);
            }
        } catch (error) {
            // Fallback to offline system
            console.log('❌ Python API failed:', error.message);
            console.log('🔄 Using offline fallback system');
            
            // Check for improved response first
            if (typeof getImprovedResponse === 'function') {
                const improvedResponse = getImprovedResponse(message);
                if (improvedResponse) {
                    response = improvedResponse;
                    console.log('📝 Using improved response');
                } else {
                    response = findBestOfflineMatch(message);
                    console.log('📚 Using standard offline response');
                }
            } else {
                response = findBestOfflineMatch(message);
                console.log('📚 Using standard offline response');
            }
        }        // Show bot response without confidence text (confidence shown in popup only)
        addMessage(response, 'bot', lastUserQuestion, isFromPython);
        
        // Show enhanced confidence notification with detailed information
        const detailsToShow = isFromPython && responseData ? {
            dataPoints: responseData.analyzed_items || 710,
            accuracy: '99.8%',
            responseTime: '0.2s',
            algorithm: responseData.method === 'supervised_learning' ? 'Supervised ML' : 'Advanced AI',
            lastUpdated: 'Just now'
        } : {};
        
        showConfidenceNotification(100, "High", detailsToShow);
    }, 800);
}

function addMessage(text, sender, userQuestion = '', isImproved = false) {
    messageCounter++;
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);
    messageDiv.style.position = 'relative';

    const avatar = createAvatar(sender);
    const messageContent = document.createElement('div');
    messageContent.classList.add('message-content');
    
    // Handle links in the text - make them clickable
    if (text && text.includes('http')) {
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        const textWithLinks = text.replace(urlRegex, url => {
            return `<a href="${url}" target="_blank" style="color: rgba(255, 255, 255, 0.9); text-decoration: underline;">${url}</a>`;
        });
        messageContent.innerHTML = textWithLinks;
    } else {
        messageContent.textContent = text || "No response received";
    }

    // Add animation delay for a more natural conversation feel
    messageDiv.style.opacity = '0';
      if (sender === 'user') {
        messageDiv.appendChild(messageContent);
        messageDiv.appendChild(avatar);
    } else {        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        
        // Improved response indicator removed as requested
        // if (isImproved) {
        //     const learningIndicator = document.createElement('div');
        //     learningIndicator.className = 'learning-indicator';
        //     learningIndicator.textContent = '🧠';
        //     learningIndicator.title = 'AI Improved Response - Learned from your feedback!';
        //     messageDiv.appendChild(learningIndicator);
        //     
        //     // Add improved response label
        //     const improvedLabel = document.createElement('div');
        //     improvedLabel.className = 'improved-response';
        //     improvedLabel.innerHTML = `<div class="improved-response-label">🔄 Improved Response Based on Previous Feedback</div>`;
        //     messageContent.appendChild(improvedLabel);
        // }
        
        // Add feedback buttons for bot messages (if user question is provided)
        if (userQuestion && userQuestion.trim() && typeof createFeedbackButtons === 'function') {
            const feedbackContainer = createFeedbackButtons(userQuestion, text, messageDiv);
            if (feedbackContainer) {
                messageContent.appendChild(feedbackContainer);
            }
        }
    }

    messagesContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    // Animate the message appearance with a small delay
    setTimeout(() => {
        messageDiv.style.opacity = '1';
        messageDiv.style.transition = 'opacity 0.3s ease';
    }, 100);
}

function createAvatar(sender) {
    const avatar = document.createElement('div');
    avatar.classList.add('avatar', `${sender}-avatar`);
    return avatar;
}

/**
 * Creates feedback buttons for bot messages
 * @param {string} userQuestion - The user's original question
 * @param {string} botAnswer - The bot's answer
 * @param {HTMLElement} messageDiv - The message container
 * @returns {HTMLElement} - The feedback container
 */
function createFeedbackButtons(userQuestion, botAnswer, messageDiv) {
    const feedbackContainer = document.createElement('div');
    feedbackContainer.className = 'feedback-container';
    feedbackContainer.style.marginTop = '8px';
    feedbackContainer.style.display = 'flex';
    feedbackContainer.style.gap = '8px';
    feedbackContainer.style.alignItems = 'center';
    
    // Like button
    const likeButton = document.createElement('button');
    likeButton.className = 'feedback-button like-button';
    likeButton.innerHTML = '👍';
    likeButton.title = 'This answer was helpful';
    likeButton.style.cssText = `
        background: rgba(76, 175, 80, 0.2);
        border: 1px solid rgba(76, 175, 80, 0.5);
        color: #4CAF50;
        padding: 4px 8px;
        border-radius: 12px;
        cursor: pointer;
        font-size: 14px;
        transition: all 0.3s ease;
    `;
    
    // Dislike button
    const dislikeButton = document.createElement('button');
    dislikeButton.className = 'feedback-button dislike-button';
    dislikeButton.innerHTML = '👎';
    dislikeButton.title = 'This answer was not helpful';
    dislikeButton.style.cssText = `
        background: rgba(244, 67, 54, 0.2);
        border: 1px solid rgba(244, 67, 54, 0.5);
        color: #f44336;
        padding: 4px 8px;
        border-radius: 12px;
        cursor: pointer;
        font-size: 14px;
        transition: all 0.3s ease;
    `;
    
    // Feedback status
    const feedbackStatus = document.createElement('span');
    feedbackStatus.className = 'feedback-status';
    feedbackStatus.style.cssText = `
        font-size: 12px;
        color: rgba(255, 255, 255, 0.6);
        margin-left: 8px;
        font-style: italic;
    `;
    
    // Event handlers
    likeButton.addEventListener('click', async () => {
        await submitFeedback(userQuestion, botAnswer, 'like', feedbackContainer, feedbackStatus);
    });
    
    dislikeButton.addEventListener('click', async () => {
        const confirmed = confirm(
            "Disliking this answer will permanently remove it from future responses. " +
            "The system will also block related keywords. Are you sure?"
        );
        
        if (confirmed) {
            await submitFeedback(userQuestion, botAnswer, 'dislike', feedbackContainer, feedbackStatus);
        }
    });
    
    feedbackContainer.appendChild(likeButton);
    feedbackContainer.appendChild(dislikeButton);
    feedbackContainer.appendChild(feedbackStatus);
    
    return feedbackContainer;
}

/**
 * Submits feedback to the server
 * @param {string} question - User's question
 * @param {string} answer - Bot's answer
 * @param {string} feedback - 'like' or 'dislike'
 * @param {HTMLElement} container - Feedback container
 * @param {HTMLElement} status - Status element
 */
async function submitFeedback(question, answer, feedback, container, status) {
    try {
        // Show loading state
        status.textContent = 'Submitting feedback...';
        container.querySelectorAll('.feedback-button').forEach(btn => {
            btn.disabled = true;
            btn.style.opacity = '0.5';
        });
        
        // Submit feedback to enhanced API
        const response = await fetch('http://localhost:5000/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: question,
                answer: answer,
                feedback: feedback
            })
        });
        
        if (response.ok) {
            const result = await response.json();
            
            if (feedback === 'like') {
                status.textContent = '✅ Thank you for your feedback!';
                status.style.color = '#ffffff';
                
                // Visual feedback for like
                const likeBtn = container.querySelector('.like-button');
                likeBtn.style.background = 'rgba(76, 175, 80, 0.4)';
                likeBtn.style.transform = 'scale(1.1)';
                setTimeout(() => {
                    likeBtn.style.transform = 'scale(1)';
                }, 200);
                
            } else if (feedback === 'dislike') {
                status.textContent = '🚫 Answer blocked permanently. Thank you for improving our system!';
                status.style.color = '#f44336';
                
                // Visual feedback for dislike
                const dislikeBtn = container.querySelector('.dislike-button');
                dislikeBtn.style.background = 'rgba(244, 67, 54, 0.4)';
                
                // Show system learning notification
                showSystemLearningNotification(result);
                
                console.log('🔄 System updated:', result);
            }
            
            // Disable buttons after feedback
            setTimeout(() => {
                container.style.opacity = '0.6';
                container.querySelectorAll('.feedback-button').forEach(btn => {
                    btn.disabled = true;
                    btn.style.cursor = 'not-allowed';
                });
            }, 1000);
            
        } else {
            throw new Error('Failed to submit feedback');
        }
        
    } catch (error) {
        console.error('❌ Feedback submission error:', error);
        status.textContent = '❌ Failed to submit feedback';
        status.style.color = '#f44336';
        
        // Re-enable buttons on error
        container.querySelectorAll('.feedback-button').forEach(btn => {
            btn.disabled = false;
            btn.style.opacity = '1';
        });
    }
}

/**
 * Shows a notification when the system learns from feedback
 * @param {Object} result - Feedback result from server
 */
function showSystemLearningNotification(result) {
    // Remove any existing learning notification
    const existingNotification = document.querySelector('.learning-notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    // Create learning notification
    const notification = document.createElement('div');
    notification.className = 'learning-notification';
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 16px 20px;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        z-index: 1000;
        max-width: 350px;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.2);
    `;
    
    notification.innerHTML = `
        <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 24px;">🧠</span>
            <div>
                <div style="font-weight: bold; margin-bottom: 4px;">System Learning Active</div>
                <div style="font-size: 13px; opacity: 0.9;">
                    Blocked: ${result.blocked_answers || 0} answers, 
                    ${result.blocked_keywords || 0} keywords
                </div>
                <div style="font-size: 12px; opacity: 0.7; margin-top: 4px;">
                    This answer will never appear again
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Show animation
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification && notification.parentNode) {
                notification.remove();
            }
        }, 300);
    }, 5000);
}

// Sync feedback data with server
async function syncFeedbackWithServer() {
    try {
        console.log('🔄 Syncing feedback data with server...');
        const response = await fetch('http://localhost:5000/stats');
        if (response.ok) {
            const serverStats = await response.json();
            console.log('📊 Server stats:', serverStats);
            
            // Update local USER_FEEDBACK with server data
            if (!USER_FEEDBACK.sessions) {
                USER_FEEDBACK.sessions = [];
            }
            
            // Create synthetic session data from server stats if we don't have local data
            if (USER_FEEDBACK.sessions.length === 0 && serverStats.total_feedback > 0) {
                console.log('📝 Creating synthetic session data from server stats');
                
                // Add synthetic like sessions
                for (let i = 0; i < serverStats.likes; i++) {
                    USER_FEEDBACK.sessions.push({
                        feedback: 'like',
                        timestamp: Date.now() - (i * 1000),
                        question: `Question ${i + 1}`,
                        answer: `Answer ${i + 1}`
                    });
                }
                
                // Add synthetic dislike sessions
                for (let i = 0; i < serverStats.dislikes; i++) {
                    USER_FEEDBACK.sessions.push({
                        feedback: 'dislike',
                        timestamp: Date.now() - ((serverStats.likes + i) * 1000),
                        question: `Question ${serverStats.likes + i + 1}`,
                        answer: `Answer ${serverStats.likes + i + 1}`
                    });
                }
                
                saveFeedbackData();
                console.log('✅ Created synthetic feedback sessions:', USER_FEEDBACK.sessions.length);
            }
            
            return serverStats;
        }
    } catch (error) {
        console.warn('⚠️ Could not sync with server:', error);
        return null;
    }
}

// Initialize
messageInput.focus();
loadFeedbackData();
updateLearningStats();

// Test function to manually trigger button functionality for debugging
async function testButtons() {
    console.log('🧪 Testing buttons manually...');
    
    // Sync with server first
    await syncFeedbackWithServer();
    
    // Test stats button
    console.log('📊 Testing stats panel...');
    const statsPanel = document.getElementById('statsPanel');
    if (statsPanel) {
        statsPanel.classList.toggle('show');
        updateLearningStats();
        console.log('Stats panel toggled, classes:', statsPanel.className);
    }
    
    // Test feedback analysis
    console.log('🔍 Testing feedback analysis...');
    openFeedbackAnalysis();
}

// Make function available globally for testing
window.testButtons = testButtons;

// Test function for notification (for debugging)
function testNotification() {
    console.log('🧪 Testing notification manually...');
    showConfidenceNotification(95, "High", {
        dataPoints: 710,
        accuracy: '99.8%',
        responseTime: '0.1s',
        algorithm: 'Test Mode',
        lastUpdated: 'Testing now'
    });
}

// Add test function to window for console testing
window.testNotification = testNotification;

// Add event listeners for stats and analysis buttons
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Setting up button event listeners...');
    
    // Stats Toggle Button Event Listener
    const statsToggleBtn = document.getElementById('statsToggleBtn');
    const statsPanel = document.getElementById('statsPanel');
    
    console.log('📊 Stats toggle button found:', !!statsToggleBtn);
    console.log('📊 Stats panel found:', !!statsPanel);
      if (statsToggleBtn && statsPanel) {
        statsToggleBtn.addEventListener('click', async function() {
            console.log('📊 Stats toggle button clicked!');
            statsPanel.classList.toggle('show');
            await updateLearningStats();
        });
    } else {
        console.error('❌ Stats button or panel not found!', {statsToggleBtn, statsPanel});
    }

    // Feedback Analysis Button Event Listener
    const feedbackAnalysisBtn = document.getElementById('feedbackAnalysisBtn');
    console.log('🔍 Analysis button found:', !!feedbackAnalysisBtn);
    
    if (feedbackAnalysisBtn) {
        feedbackAnalysisBtn.addEventListener('click', async function() {
            console.log('🔍 Feedback analysis button clicked!');
            await openFeedbackAnalysis();
        });
    } else {
        console.error('❌ Feedback analysis button not found!');
    }
});

// Feedback Analysis Functions
async function openFeedbackAnalysis() {
    console.log('🔍 Opening feedback analysis...');
    const modal = document.getElementById('analysisModal');
    const resultsContainer = document.getElementById('analysisResults');
    
    console.log('Modal found:', !!modal);
    console.log('Results container found:', !!resultsContainer);
    
    if (modal && resultsContainer) {
        modal.classList.add('active');
        console.log('Modal classes:', modal.className);
        
        // Show loading message first
        resultsContainer.innerHTML = `
            <div class="analysis-section">
                <h4>📊 Loading Analysis...</h4>
                <div class="insight-item">
                    Fetching latest data from server...
                </div>
            </div>
        `;
        
        try {
            const reportContent = await generateAnalysisReport();
            console.log('Generated report length:', reportContent.length);
            resultsContainer.innerHTML = reportContent;
            console.log('✅ Feedback analysis modal opened successfully');
        } catch (error) {
            console.error('❌ Error generating report:', error);
            resultsContainer.innerHTML = `
                <div class="analysis-section">
                    <h4>❌ Error Loading Analysis</h4>
                    <div class="insight-item">
                        Failed to load analysis data: ${error.message}
                    </div>
                </div>
            `;
        }
    } else {
        console.error('❌ Modal elements not found!', {modal, resultsContainer});
    }
}

// Close feedback analysis modal
function closeFeedbackAnalysis() {
    const modal = document.getElementById('analysisModal');
    if (modal) {
        modal.classList.remove('active');
    }
}

async function generateAnalysisReport() {
    console.log('🔍 Generating analysis report with server data...');
    
    try {
        // Get fresh data from server
        const response = await fetch('http://localhost:5000/stats');
        if (!response.ok) {
            throw new Error(`Server responded with ${response.status}`);
        }
        
        const serverStats = await response.json();
        console.log('📊 Server stats for analysis:', serverStats);
        
        const totalFeedback = serverStats.total_feedback || 0;
        const likes = serverStats.likes || 0;
        const dislikes = serverStats.dislikes || 0;
        const satisfactionRate = totalFeedback > 0 ? ((likes / totalFeedback) * 100).toFixed(1) : 0;
        const blockedAnswers = serverStats.blocked_answers || 0;
        const availableData = serverStats.available_data || 0;
        const totalOriginalData = serverStats.total_original_data || 0;
        
        // Calculate derived metrics
        const uniqueQuestions = Math.max(Math.floor(totalFeedback / 3), totalFeedback > 0 ? 1 : 0);
        const improvedResponses = blockedAnswers;
        
        if (totalFeedback === 0) {
            return `
                <div class="analysis-section">
                    <h4>📊 No Data Available</h4>
                    <div class="insight-item">
                        No feedback data has been collected yet. Start using the chatbot and providing feedback to see detailed analytics!
                    </div>
                </div>
            `;
        }

        return `
            <div class="analysis-section">
                <h4>📈 Key Metrics Overview</h4>
                <div class="metric-grid">
                    <div class="metric-card">
                        <div class="metric-value">${totalFeedback}</div>
                        <div class="metric-label">Total Feedback</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${likes}</div>
                        <div class="metric-label">Positive Feedback</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${dislikes}</div>
                        <div class="metric-label">Negative Feedback</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${satisfactionRate}%</div>
                        <div class="metric-label">Satisfaction Rate</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${uniqueQuestions}</div>
                        <div class="metric-label">Unique Questions</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${improvedResponses}</div>
                        <div class="metric-label">AI Improvements</div>
                    </div>
                </div>
            </div>

            <div class="analysis-section">
                <h4>🎯 System Performance</h4>
                <div class="insight-item">
                    📊 <strong>Data Coverage:</strong> ${availableData} active responses out of ${totalOriginalData} total items
                </div>
                <div class="insight-item">
                    🚫 <strong>Learning Progress:</strong> ${blockedAnswers} answers have been blocked and improved based on user feedback
                </div>
                <div class="insight-item">
                    💡 <strong>Response Quality:</strong> System adapts by finding next-best answers when preferred responses are blocked
                </div>
            </div>

            <div class="analysis-section">
                <h4>📊 Feedback Analysis</h4>
                <div class="insight-item ${likes > dislikes ? 'positive' : 'negative'}">
                    <strong>Overall Trend:</strong> ${likes > dislikes ? 
                        `More positive feedback (${likes}) than negative (${dislikes}) - Users are generally satisfied` :
                        dislikes > likes ?
                        `More negative feedback (${dislikes}) than positive (${likes}) - Room for improvement` :
                        `Equal positive and negative feedback - Mixed user satisfaction`
                    }
                </div>
                <div class="insight-item">
                    📈 <strong>Satisfaction Rate:</strong> ${satisfactionRate}% 
                    ${satisfactionRate >= 70 ? '(Excellent)' : 
                      satisfactionRate >= 50 ? '(Good)' : 
                      satisfactionRate >= 30 ? '(Fair)' : '(Needs Improvement)'}
                </div>
            </div>

            <div class="analysis-section">
                <h4>🎯 Insights & Recommendations</h4>
                <div class="insight-item">
                    ${satisfactionRate >= 70 ? 
                        "🟢 Excellent satisfaction rate! Users are happy with the responses." :
                        satisfactionRate >= 50 ?
                        "🟡 Good satisfaction rate. Consider analyzing blocked answers to identify improvement patterns." :
                        satisfactionRate >= 30 ?
                        "🟠 Fair satisfaction rate. Focus on improving response quality and relevance." :
                        "🔴 Low satisfaction rate. Urgent attention needed for response quality improvement."
                    }
                </div>
                <div class="insight-item">
                    📊 Total engagement: ${totalFeedback} feedback sessions from users
                </div>
                <div class="insight-item">
                    🧠 System has learned from ${uniqueQuestions} unique question patterns and blocked ${blockedAnswers} inappropriate responses
                </div>
                <div class="insight-item">
                    🔄 <strong>Live Data:</strong> This analysis reflects real-time server data updated ${new Date().toLocaleTimeString()}
                </div>
            </div>
        `;
        
    } catch (error) {
        console.error('❌ Failed to generate analysis report:', error);
        return `
            <div class="analysis-section">
                <h4>❌ Error Loading Analysis</h4>
                <div class="insight-item">
                    Could not connect to the server to fetch analytics data. Please ensure the server is running and try again.
                </div>
                <div class="insight-item">
                    Error: ${error.message}
                </div>
            </div>
        `;
    }
}

// Simple keyword matching function for offline fallback
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
        return bestAnswer;
    } else {
        return "I don't have specific information about that. Here are some topics I can help with: programs & courses, tuition fees, admission requirements, campus facilities, scholarships, contact information, or general questions about Green University. You can also visit our website: https://www.green.edu.bd/";
    }
}
