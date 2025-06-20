// Initialize global variables first
        let USER_FEEDBACK = {
            sessions: [],
            questionFeedback: {},
            patternScores: {},
            improvedResponses: {}
        };

        let lastUserQuestion = '';
        let messageCounter = 0;

        // Feedback Learning System// Load saved feedback data
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

        // Extract patterns from user questions
        function extractQuestionPatterns(question) {
            const patterns = [];
            const lowerQuestion = question.toLowerCase().trim();
            
            // Question type patterns
            if (lowerQuestion.startsWith('what')) patterns.push('what_question');
            if (lowerQuestion.startsWith('how')) patterns.push('how_question');
            if (lowerQuestion.startsWith('when')) patterns.push('when_question');
            if (lowerQuestion.startsWith('where')) patterns.push('where_question');
            if (lowerQuestion.startsWith('why')) patterns.push('why_question');
            if (lowerQuestion.startsWith('who')) patterns.push('who_question');
            if (lowerQuestion.includes('?')) patterns.push('general_question');
            
            // Content patterns
            const keywords = ['fee', 'cost', 'price', 'tuition', 'admission', 'program', 'course', 
                             'department', 'faculty', 'student', 'university', 'college', 'degree',
                             'semester', 'credit', 'requirement', 'eligibility', 'application'];
            
            keywords.forEach(keyword => {
                if (lowerQuestion.includes(keyword)) {
                    patterns.push(`contains_${keyword}`);
                }
            });
            
            return patterns;
        }

        // Create feedback buttons
        function createFeedbackButtons(userQuestion, botAnswer, messageElement) {
            // Don't add feedback to welcome messages
            if (botAnswer.includes('Welcome to Green University') || 
                botAnswer.includes('I\'m ready to answer')) {
                return null;
            }
            
            const feedbackContainer = document.createElement('div');
            feedbackContainer.className = 'feedback-container';
            feedbackContainer.innerHTML = `
                <div class="feedback-buttons">
                    <button class="feedback-btn like-btn" data-feedback="like" title="This response was helpful">
                        👍 Helpful
                    </button>
                    <button class="feedback-btn dislike-btn" data-feedback="dislike" title="This response was not helpful">
                        👎 Not helpful
                    </button>
                </div>
            `;
            
            const likeBtn = feedbackContainer.querySelector('.like-btn');
            const dislikeBtn = feedbackContainer.querySelector('.dislike-btn');
            
            likeBtn.addEventListener('click', () => {
                recordFeedback(userQuestion, botAnswer, 'like', messageElement);
            });
            
            dislikeBtn.addEventListener('click', () => {
                recordFeedback(userQuestion, botAnswer, 'dislike', messageElement);
            });
              return feedbackContainer;
        }
        
        // Record user feedback and learn patterns
        function recordFeedback(userQuestion, botAnswer, feedbackType, messageElement) {
            // Ensure USER_FEEDBACK is properly initialized
            if (!USER_FEEDBACK || typeof USER_FEEDBACK !== 'object') {
                USER_FEEDBACK = {
                    sessions: [],
                    questionFeedback: {},
                    patternScores: {},
                    improvedResponses: {}
                };
            }
            
            // Ensure sessions array exists
            if (!USER_FEEDBACK.sessions || !Array.isArray(USER_FEEDBACK.sessions)) {
                USER_FEEDBACK.sessions = [];
            }
            
            // Ensure other properties exist
            if (!USER_FEEDBACK.questionFeedback) USER_FEEDBACK.questionFeedback = {};
            if (!USER_FEEDBACK.patternScores) USER_FEEDBACK.patternScores = {};
            if (!USER_FEEDBACK.improvedResponses) USER_FEEDBACK.improvedResponses = {};
            
            const timestamp = new Date().toISOString();
            const sessionId = 'session_' + Date.now();
            
            // Create feedback entry
            const feedbackEntry = {
                timestamp,
                userQuestion,
                botAnswer,
                feedback: feedbackType,
                sessionId
            };
            
            USER_FEEDBACK.sessions.push(feedbackEntry);
            
            // Extract patterns and update scores
            const patterns = extractQuestionPatterns(userQuestion);
            patterns.forEach(pattern => {
                if (!USER_FEEDBACK.patternScores[pattern]) {
                    USER_FEEDBACK.patternScores[pattern] = { likes: 0, dislikes: 0 };
                }
                
                if (feedbackType === 'like') {
                    USER_FEEDBACK.patternScores[pattern].likes++;
                } else {
                    USER_FEEDBACK.patternScores[pattern].dislikes++;
                }
            });
              // Track question-specific feedback
            const questionKey = userQuestion.toLowerCase().trim();
            if (!USER_FEEDBACK.questionFeedback[questionKey]) {
                USER_FEEDBACK.questionFeedback[questionKey] = {
                    likes: 0,
                    dislikes: 0,
                    responses: [],
                    bestAnswer: null,
                    patterns: patterns
                };
            }
            
            // Ensure responses array exists
            if (!USER_FEEDBACK.questionFeedback[questionKey].responses || !Array.isArray(USER_FEEDBACK.questionFeedback[questionKey].responses)) {
                USER_FEEDBACK.questionFeedback[questionKey].responses = [];
            }
            
            USER_FEEDBACK.questionFeedback[questionKey].responses.push({
                answer: botAnswer,
                feedback: feedbackType,
                timestamp
            });
              if (feedbackType === 'like') {
                USER_FEEDBACK.questionFeedback[questionKey].likes++;
                USER_FEEDBACK.questionFeedback[questionKey].bestAnswer = botAnswer;
            } else {
                USER_FEEDBACK.questionFeedback[questionKey].dislikes++;
                  // Use the enhanced alternative response search
                const improvedResponse = handleDislikeFeedback(userQuestion, botAnswer);
                
                // Immediately provide the improved response to user
                if (improvedResponse && improvedResponse !== botAnswer) {
                    // Add the improved response as a new message
                    setTimeout(() => {                        if (typeof addMessage === 'function') {
                            setTimeout(() => {
                                addMessage(improvedResponse, 'bot', userQuestion, true);
                            }, 500);
                        } else {
                            // Fallback: show alert if addMessage is not available
                            console.log("Improved response:", improvedResponse);
                        }
                    }, 1500);
                }
            }
              saveFeedbackData();
            updateFeedbackUI(messageElement, feedbackType);
            updateLearningStats();
            
            // Show search indicator for dislikes
            if (feedbackType === 'dislike') {
                showAlternativeSearchFeedback(messageElement);
            }
            
            console.log(`Recorded ${feedbackType} feedback for: "${userQuestion}"`);
        }

        // Generate improved response when user dislikes an answer
        function generateImprovedResponse(userQuestion, dislikedAnswer, patterns) {
            const questionKey = userQuestion.toLowerCase().trim();
            
            // Create improved response based on patterns and common questions
            let improvedAnswer = '';
            
            // Pattern-based improvements
            if (patterns.includes('contains_fee') || patterns.includes('contains_cost') || patterns.includes('contains_tuition')) {
                improvedAnswer = "For detailed information about fees and tuition costs at Green University of Bangladesh, please visit our official website at https://www.green.edu.bd/ or contact our admissions office directly. Our fee structure varies by program and we offer various payment plans and scholarships.";
            } else if (patterns.includes('contains_admission') || patterns.includes('contains_application')) {
                improvedAnswer = "For admission requirements and application procedures at Green University of Bangladesh, please check our admissions portal at https://www.green.edu.bd/. We have different requirements for different programs. You can also visit our campus or call our admissions hotline for personalized guidance.";
            } else if (patterns.includes('contains_program') || patterns.includes('contains_course')) {
                improvedAnswer = "Green University of Bangladesh offers a wide range of undergraduate and graduate programs across various disciplines including Engineering, Business, Computer Science, and more. For detailed program information, curriculum, and requirements, please visit https://www.green.edu.bd/ or contact our academic advisors.";
            } else if (patterns.includes('contains_department') || patterns.includes('contains_faculty')) {
                improvedAnswer = "Green University has several academic departments with experienced faculty members. For information about specific departments, faculty profiles, and their expertise areas, please visit our website at https://www.green.edu.bd/ or contact the relevant department directly.";
            } else {
                // Generic improved response
                improvedAnswer = "I apologize that my previous response wasn't helpful. For the most accurate and detailed information about Green University of Bangladesh, I recommend visiting our official website at https://www.green.edu.bd/ or contacting our student services directly. They can provide you with personalized assistance for your specific inquiry.";
            }
            
            // Store the improved response
            if (!USER_FEEDBACK.improvedResponses[questionKey]) {
                USER_FEEDBACK.improvedResponses[questionKey] = [];
            }
            
            USER_FEEDBACK.improvedResponses[questionKey].push({
                originalAnswer: dislikedAnswer,
                improvedAnswer: improvedAnswer,
                patterns: patterns,
                timestamp: new Date().toISOString()
            });
            
            console.log(`Generated improved response for: "${userQuestion}"`);
        }        // Get improved response for a question if available
        function getImprovedResponse(userQuestion) {
            const questionKey = userQuestion.toLowerCase().trim();
            
            // Check if we have improved responses for this question
            if (USER_FEEDBACK.improvedResponses[questionKey]) {
                const improvements = USER_FEEDBACK.improvedResponses[questionKey];
                if (improvements.length > 0) {
                    // Get the latest improvement (prioritize alternative search results)
                    const latestImprovement = improvements[improvements.length - 1];
                    return latestImprovement.improvedAnswer;
                }
            }
            
            // Check if we have feedback data for this question
            if (USER_FEEDBACK.questionFeedback[questionKey]) {
                const feedback = USER_FEEDBACK.questionFeedback[questionKey];
                
                // If question has a proven good answer (more likes than dislikes), use it
                if (feedback.likes > feedback.dislikes && feedback.bestAnswer) {
                    return feedback.bestAnswer;
                }
            }
            
            // Check for similar questions that have good responses
            const similarQuestions = findSimilarQuestions(userQuestion);
            for (const similarQ of similarQuestions) {
                if (USER_FEEDBACK.questionFeedback[similarQ] && 
                    USER_FEEDBACK.questionFeedback[similarQ].bestAnswer &&
                    USER_FEEDBACK.questionFeedback[similarQ].likes > USER_FEEDBACK.questionFeedback[similarQ].dislikes) {
                    return USER_FEEDBACK.questionFeedback[similarQ].bestAnswer;
                }
            }
            
            return null;
        }

        // Find similar questions based on keywords
        function findSimilarQuestions(userQuestion) {
            const input = userQuestion.toLowerCase().trim();
            const inputWords = input.split(' ').filter(word => word.length > 3);
            const similarQuestions = [];
            
            for (const questionKey in USER_FEEDBACK.questionFeedback) {
                let similarity = 0;
                const questionWords = questionKey.split(' ');
                
                for (const inputWord of inputWords) {
                    for (const questionWord of questionWords) {
                        if (inputWord === questionWord || 
                            inputWord.includes(questionWord) || 
                            questionWord.includes(inputWord)) {
                            similarity++;
                        }
                    }
                }
                
                if (similarity > 0) {
                    similarQuestions.push(questionKey);
                }
            }            
            return similarQuestions;
        }

        // Update feedback UI
        function updateFeedbackUI(messageElement, feedbackType) {
            const feedbackButtons = messageElement.querySelectorAll('.feedback-btn');
            feedbackButtons.forEach(btn => {
                btn.disabled = true;
                if (btn.dataset.feedback === feedbackType) {
                    btn.classList.add('selected');
                    btn.innerHTML = feedbackType === 'like' ? '👍 Liked' : '👎 Disliked';
                } else {
                    btn.style.opacity = '0.5';
                }
            });
            
            const thankYou = document.createElement('div');
            thankYou.className = 'feedback-thanks';
            if (feedbackType === 'like') {
                thankYou.innerHTML = `<small>✨ Thank you! Your positive feedback helps me learn.</small>`;
            } else {
                thankYou.innerHTML = `<small>🔄 Thank you! I'll remember this and provide better responses next time.</small>`;
            }
            messageElement.appendChild(thankYou);
        }        // Update learning statistics
        function updateLearningStats() {
            // Ensure USER_FEEDBACK exists and has proper structure
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
            
            const totalFeedback = sessions.length;
            const likes = sessions.filter(s => s && s.feedback === 'like').length;
            const dislikes = totalFeedback - likes;
            const satisfactionRate = totalFeedback > 0 ? (likes / totalFeedback * 100).toFixed(1) : 0;
            const uniqueQuestions = Object.keys(questionFeedback).length;
            const improvedResponseCount = Object.keys(improvedResponses).length;
            
            const elements = {
                totalFeedback: document.getElementById('totalFeedback'),
                totalLikes: document.getElementById('totalLikes'),
                totalDislikes: document.getElementById('totalDislikes'),
                satisfactionRate: document.getElementById('satisfactionRate'),
                uniqueQuestions: document.getElementById('uniqueQuestions'),
                improvedResponses: document.getElementById('improvedResponses'),
                satisfactionFill: document.getElementById('satisfactionFill')
            };
            
            if (elements.totalFeedback) elements.totalFeedback.textContent = totalFeedback;
            if (elements.totalLikes) elements.totalLikes.textContent = likes;
            if (elements.totalDislikes) elements.totalDislikes.textContent = dislikes;
            if (elements.satisfactionRate) elements.satisfactionRate.textContent = satisfactionRate + '%';
            if (elements.uniqueQuestions) elements.uniqueQuestions.textContent = uniqueQuestions;
            if (elements.improvedResponses) elements.improvedResponses.textContent = improvedResponseCount;
            if (elements.satisfactionFill) elements.satisfactionFill.style.width = satisfactionRate + '%';
        }        // Export feedback data
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

        // Initialize feedback system
        document.addEventListener('DOMContentLoaded', function() {
            loadFeedbackData();
              const statsToggleBtn = document.getElementById('statsToggleBtn');
            const statsPanel = document.getElementById('statsPanel');
            
            if (statsToggleBtn && statsPanel) {
                statsToggleBtn.addEventListener('click', function() {
                    statsPanel.classList.toggle('show');
                    updateLearningStats();
                });
            }

            // Feedback Analysis Button Event Listener
            const feedbackAnalysisBtn = document.getElementById('feedbackAnalysisBtn');
            if (feedbackAnalysisBtn) {
                feedbackAnalysisBtn.addEventListener('click', openFeedbackAnalysis);
            }
            
            updateLearningStats();
        });

        // Feedback Analysis Functions
        function openFeedbackAnalysis() {
            const modal = document.getElementById('analysisModal');
            const resultsContainer = document.getElementById('analysisResults');
            
            modal.classList.add('active');
            resultsContainer.innerHTML = generateAnalysisReport();
        }

        function closeFeedbackAnalysis() {
            const modal = document.getElementById('analysisModal');
            modal.classList.remove('active');
        }

        function generateAnalysisReport() {
            const data = USER_FEEDBACK;
            const totalSessions = data.sessions ? data.sessions.length : 0;
            
            if (totalSessions === 0) {
                return `
                    <div class="analysis-section">
                        <h4>📊 No Data Available</h4>
                        <div class="insight-item">
                            No feedback data has been collected yet. Start using the chatbot and providing feedback to see detailed analytics!
                        </div>
                    </div>
                `;
            }

            // Calculate metrics
            const likes = data.sessions.filter(s => s.feedback === 'like').length;
            const dislikes = data.sessions.filter(s => s.feedback === 'dislike').length;
            const satisfactionRate = totalSessions > 0 ? ((likes / totalSessions) * 100).toFixed(1) : 0;
            const uniqueQuestions = Object.keys(data.questionFeedback || {}).length;
            const improvedResponses = Object.keys(data.improvedResponses || {}).length;

            // Most liked topics
            const topLikedQuestions = Object.entries(data.questionFeedback || {})
                .filter(([q, data]) => data.likes > 0)
                .sort((a, b) => b[1].likes - a[1].likes)
                .slice(0, 5);

            // Most disliked topics
            const topDislikedQuestions = Object.entries(data.questionFeedback || {})
                .filter(([q, data]) => data.dislikes > 0)
                .sort((a, b) => b[1].dislikes - a[1].dislikes)
                .slice(0, 5);

            // Pattern analysis
            const patternInsights = analyzePatterns(data.patternScores || {});

            return `
                <div class="analysis-section">
                    <h4>📈 Key Metrics Overview</h4>
                    <div class="metric-grid">
                        <div class="metric-card">
                            <div class="metric-value">${totalSessions}</div>
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
                    <h4>👍 Most Appreciated Topics</h4>
                    ${topLikedQuestions.length > 0 ? 
                        topLikedQuestions.map(([question, data]) => `
                            <div class="insight-item">
                                <strong>"${question}"</strong> - ${data.likes} likes, ${data.dislikes} dislikes
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: ${(data.likes / (data.likes + data.dislikes)) * 100}%"></div>
                                </div>
                            </div>
                        `).join('') :
                        '<div class="insight-item">No liked questions yet.</div>'
                    }
                </div>

                <div class="analysis-section">
                    <h4>👎 Areas for Improvement</h4>
                    ${topDislikedQuestions.length > 0 ? 
                        topDislikedQuestions.map(([question, data]) => `
                            <div class="insight-item">
                                <strong>"${question}"</strong> - ${data.dislikes} dislikes, ${data.likes} likes
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: ${data.likes > 0 ? (data.likes / (data.likes + data.dislikes)) * 100 : 0}%; background: linear-gradient(90deg, #ef4444 0%, #f87171 100%);"></div>
                                </div>
                            </div>
                        `).join('') :
                        '<div class="insight-item">No negative feedback yet.</div>'
                    }
                </div>

                <div class="analysis-section">
                    <h4>🧠 Pattern Insights</h4>
                    ${patternInsights.length > 0 ? 
                        patternInsights.map(insight => `<div class="insight-item">${insight}</div>`).join('') :
                        '<div class="insight-item">Not enough data for pattern analysis yet.</div>'
                    }
                </div>

                <div class="analysis-section">
                    <h4>💾 Data Export Options</h4>
                    <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                        <button class="export-btn" onclick="exportDetailedAnalysis()" style="margin: 0;">
                            📊 Export Analysis Report
                        </button>
                        <button class="export-btn" onclick="exportRawFeedbackData()" style="margin: 0;">
                            📄 Export Raw Data
                        </button>
                        <button class="export-btn" onclick="loadFeedbackDataset()" style="margin: 0;">
                            📤 Load Dataset
                        </button>
                    </div>
                </div>
            `;
        }

        function analyzePatterns(patternScores) {
            const insights = [];
            const patterns = Object.entries(patternScores);
            
            if (patterns.length === 0) return insights;

            // Find most successful patterns
            const successfulPatterns = patterns
                .filter(([pattern, scores]) => scores.likes > scores.dislikes)
                .sort((a, b) => (b[1].likes - b[1].dislikes) - (a[1].likes - a[1].dislikes))
                .slice(0, 3);

            if (successfulPatterns.length > 0) {
                insights.push(`🎯 Most successful topic patterns: ${successfulPatterns.map(([pattern]) => `"${pattern}"`).join(', ')}`);
            }

            // Find challenging patterns
            const challengingPatterns = patterns
                .filter(([pattern, scores]) => scores.dislikes > scores.likes)
                .sort((a, b) => (b[1].dislikes - b[1].likes) - (a[1].dislikes - a[1].likes))
                .slice(0, 3);

            if (challengingPatterns.length > 0) {
                insights.push(`⚠️ Most challenging topics: ${challengingPatterns.map(([pattern]) => `"${pattern}"`).join(', ')}`);
            }

            // Overall satisfaction trend
            const totalLikes = patterns.reduce((sum, [_, scores]) => sum + scores.likes, 0);
            const totalDislikes = patterns.reduce((sum, [_, scores]) => sum + scores.dislikes, 0);
            const overallSatisfaction = totalLikes / (totalLikes + totalDislikes) * 100;

            if (overallSatisfaction > 70) {
                insights.push(`✅ High overall satisfaction rate: ${overallSatisfaction.toFixed(1)}%`);
            } else if (overallSatisfaction < 50) {
                insights.push(`🔧 Low satisfaction rate detected: ${overallSatisfaction.toFixed(1)}% - consider improving responses`);
            }

            return insights;
        }

        function exportDetailedAnalysis() {
            const analysisData = {
                timestamp: new Date().toISOString(),
                summary: generateAnalysisReport(),
                rawData: USER_FEEDBACK,
                insights: analyzePatterns(USER_FEEDBACK.patternScores || {})
            };

            const blob = new Blob([JSON.stringify(analysisData, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `greenbot_analysis_${new Date().toISOString().split('T')[0]}.json`;
            a.click();
            URL.revokeObjectURL(url);
        }

        function exportRawFeedbackData() {
            const blob = new Blob([JSON.stringify(USER_FEEDBACK, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `greenbot_feedback_${new Date().toISOString().split('T')[0]}.json`;
            a.click();
            URL.revokeObjectURL(url);
        }

        function loadFeedbackDataset() {
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = '.json';
            input.onchange = function(e) {
                const file = e.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        try {
                            const loadedData = JSON.parse(e.target.result);
                            
                            // Validate and merge data
                            if (loadedData.sessions && Array.isArray(loadedData.sessions)) {
                                USER_FEEDBACK = {
                                    sessions: [...(USER_FEEDBACK.sessions || []), ...loadedData.sessions],
                                    questionFeedback: {...(USER_FEEDBACK.questionFeedback || {}), ...(loadedData.questionFeedback || {})},
                                    patternScores: {...(USER_FEEDBACK.patternScores || {}), ...(loadedData.patternScores || {})},
                                    improvedResponses: {...(USER_FEEDBACK.improvedResponses || {}), ...(loadedData.improvedResponses || {})}
                                };
                                
                                saveFeedbackData();
                                updateLearningStats();
                                
                                alert(`Successfully loaded ${loadedData.sessions.length} feedback entries!`);
                                
                                // Refresh analysis if modal is open
                                const modal = document.getElementById('analysisModal');
                                if (modal.classList.contains('active')) {
                                    openFeedbackAnalysis();
                                }
                            } else {
                                alert('Invalid feedback data format!');
                            }
                        } catch (error) {
                            alert('Error loading feedback data: ' + error.message);
                        }
                    };
                    reader.readAsText(file);
                }
            };
            input.click();
        }

        // Close modal when clicking outside
        document.addEventListener('click', function(e) {
            const modal = document.getElementById('analysisModal');
            if (e.target === modal) {                closeFeedbackAnalysis();
            }
        });// Enhanced alternative response search system
function findAlternativeResponse(userQuestion, dislikedAnswer) {
    const input = userQuestion.toLowerCase().trim();
    const responses = [];
    
    // Check for available chatbot data sources
    let chatbotData = [];
    
    // Try to get enhanced data first, then fall back to basic data
    if (typeof ENHANCED_CHATBOT_DATA !== 'undefined' && Array.isArray(ENHANCED_CHATBOT_DATA) && ENHANCED_CHATBOT_DATA.length > 0) {
        chatbotData = ENHANCED_CHATBOT_DATA;
        console.log('Using enhanced chatbot data for alternative search');
    } else if (typeof CHATBOT_DATA !== 'undefined' && Array.isArray(CHATBOT_DATA) && CHATBOT_DATA.length > 0) {
        chatbotData = CHATBOT_DATA;
        console.log('Using basic chatbot data for alternative search');
    } else if (typeof window !== 'undefined' && window.CHATBOT_DATA && Array.isArray(window.CHATBOT_DATA) && window.CHATBOT_DATA.length > 0) {
        chatbotData = window.CHATBOT_DATA;
        console.log('Using global chatbot data for alternative search');
    } else {
        console.error('No chatbot data available for alternative response search');
        return null;
    }
    
    // Search through all available responses and score them
    for (const item of chatbotData) {
        let score = 0;
        
        // Skip the response that was already disliked
        if (item.answer === dislikedAnswer) {
            continue;
        }
        
        // Calculate semantic similarity
        if (item.keywords && Array.isArray(item.keywords)) {
            for (const keyword of item.keywords) {
                if (input.includes(keyword.toLowerCase())) {
                    score += 1.0;
                }
            }
        }
        
        // Check for question word matches
        if (item.question) {
            const questionWords = item.question.toLowerCase().split(' ');
            for (const word of questionWords) {
                if (input.includes(word) && word.length > 3) {
                    score += 0.5;
                }
            }
        }
        
        // Add partial matches
        const inputWords = input.split(' ');
        for (const inputWord of inputWords) {
            if (inputWord.length > 3 && item.keywords) {
                for (const keyword of item.keywords) {
                    if (keyword.toLowerCase().includes(inputWord) || inputWord.includes(keyword.toLowerCase())) {
                        score += 0.3;
                    }
                }
            }
        }
        
        if (score > 0) {
            responses.push({
                answer: item.answer,
                score: score,
                question: item.question
            });
        }
    }
    
    // Sort by score and return the best alternative
    responses.sort((a, b) => b.score - a.score);
    
    if (responses.length > 0) {
        return responses[0].answer;
    }
    
    // If no alternative found, return null
    return null;
}

// Enhanced feedback processing with alternative response search
function handleDislikeFeedback(userQuestion, dislikedAnswer) {
    console.log(`Processing dislike feedback for: "${userQuestion}"`);
    
    // First, try to find an alternative response
    const alternativeResponse = findAlternativeResponse(userQuestion, dislikedAnswer);
    
    if (alternativeResponse && alternativeResponse !== dislikedAnswer) {
        // Store the alternative response for future use
        const questionKey = userQuestion.toLowerCase().trim();
        
        if (!USER_FEEDBACK.improvedResponses[questionKey]) {
            USER_FEEDBACK.improvedResponses[questionKey] = [];
        }
        
        USER_FEEDBACK.improvedResponses[questionKey].push({
            originalAnswer: dislikedAnswer,
            improvedAnswer: alternativeResponse,
            type: 'alternative_search',
            timestamp: new Date().toISOString(),
            source: 'automated_search'
        });
        
        console.log(`Found alternative response for: "${userQuestion}"`);
        return alternativeResponse;
    } else {
        // No suitable alternative found, use the fallback message
        const fallbackMessage = "I apologize that my previous response wasn't helpful. For the most accurate and detailed information about Green University of Bangladesh, I recommend visiting our official website at https://www.green.edu.bd/ or contacting our student services directly. They can provide you with personalized assistance for your specific inquiry.";
        
        // Store the fallback response
        const questionKey = userQuestion.toLowerCase().trim();
        
        if (!USER_FEEDBACK.improvedResponses[questionKey]) {
            USER_FEEDBACK.improvedResponses[questionKey] = [];
        }
        
        USER_FEEDBACK.improvedResponses[questionKey].push({
            originalAnswer: dislikedAnswer,
            improvedAnswer: fallbackMessage,
            type: 'fallback_message',
            timestamp: new Date().toISOString(),
            source: 'automated_fallback'
        });
        
        console.log(`No alternative found, using fallback for: "${userQuestion}"`);
        return fallbackMessage;
    }
}

// Visual feedback for alternative response search
        function showAlternativeSearchFeedback(messageElement) {
            const searchingIndicator = document.createElement('div');
            searchingIndicator.className = 'searching-indicator';
            searchingIndicator.innerHTML = `
                <div style="
                    background: rgba(16, 185, 129, 0.1);
                    border: 1px solid rgba(16, 185, 129, 0.3);
                    border-radius: 8px;
                    padding: 8px 12px;
                    margin-top: 8px;
                    font-size: 12px;
                    color: #10b981;
                    display: flex;
                    align-items: center;
                    gap: 6px;
                ">
                    <span style="animation: spin 1s linear infinite;">🔍</span>
                    Searching for a better response...
                </div>
                <style>
                    @keyframes spin {
                        from { transform: rotate(0deg); }
                        to { transform: rotate(360deg); }
                    }
                </style>
            `;
            
            if (messageElement && messageElement.querySelector('.message-content')) {
                messageElement.querySelector('.message-content').appendChild(searchingIndicator);
                
                // Remove the indicator after a delay
                setTimeout(() => {
                    if (searchingIndicator.parentNode) {
                        searchingIndicator.remove();
                    }
                }, 2000);
            }
        }