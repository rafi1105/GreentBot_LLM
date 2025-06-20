// DOM Elements
const messagesContainer = document.getElementById('messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');

// Bot avatar image URL
const BOT_AVATAR_URL = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQaNSwgPDS-SDW_dMaphPf6UKOCUk1KUq1quQ&s';

// Server settings - DISABLED FOR PURE OFFLINE MODE
let SERVER_PORT = 5000; // Default port (not used)
const SERVER_HOST = 'http://127.0.0.1';
let isOfflineMode = true; // Always offline mode
let serverFeaturesEnabled = false; // Disable all server features

// Initialize
messageInput.focus();

// Add welcome message when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Hide server panel completely
    const serverPanel = document.getElementById('server-panel');
    if (serverPanel) {
        serverPanel.style.display = 'none';
    }
    
    // Add welcome message
    setTimeout(() => {
        addMessage("Welcome to Green University of Bangladesh chatbot! 🎓", 'bot');
        addMessage("I'm ready to answer your questions about programs, fees, admission, and more!", 'bot');
    }, 500);
});

// Bot avatar is set directly in CSS using the image URL
// No fallbacks will be used - only the specified image

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

    // Always use offline chatbot - no server functionality
    setTimeout(() => {
        // Remove typing indicator
        const indicator = document.getElementById('typing-indicator');
        if (indicator) indicator.remove();
        
        const response = findBestOfflineMatch(message);
        addMessage(response, 'bot');
    }, 800); // Realistic typing delay
}

function sendMessageToServer(message) {
    console.log("Sending message to server:", message);
    
    fetch(`${SERVER_HOST}:${SERVER_PORT}/api/chat`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
    })
    .then(response => {
        console.log("Response status:", response.status);
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        // Remove typing indicator
        const indicator = document.getElementById('typing-indicator');
        if (indicator) indicator.remove();
        
        console.log("Raw API response:", data);
        
        if (!data || typeof data !== 'object') {
            throw new Error("Invalid response format");
        }
        
        // Add bot response to chat
        const responseText = data.response || "Sorry, I didn't get a proper response.";
        console.log("Displaying response:", responseText);
        addMessage(responseText, 'bot');
    })
    .catch(error => {
        // Remove typing indicator
        const indicator = document.getElementById('typing-indicator');
        if (indicator) indicator.remove();
        
        console.error('Error:', error);
        addMessage(`I couldn't connect to the server. Please make sure the server is running at ${SERVER_HOST}:${SERVER_PORT}. You can use the "Start Server" or "Test Connection" buttons in the bottom panel.`, 'bot');
    });
}

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);

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
    } else {
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
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
    // No fallback logic - the bot avatar will only show the specified image via CSS
    return avatar;
}

// Server Control Functions
let serverCheckInterval;

// Check server status
async function checkServerStatus() {
    // Try to fetch server_port.txt first to see if server port has changed
    try {
        const portResponse = await fetch('server_port.txt');
        if (portResponse.ok) {
            const portText = await portResponse.text();
            const port = parseInt(portText.trim());
            if (!isNaN(port) && port > 0) {
                SERVER_PORT = port;
                console.log(`Using server port: ${SERVER_PORT}`);
            }
        }
    } catch (e) {
        console.log("Could not fetch server port file, using default");
    }
    
    // Now try multiple ports, starting with the current one
    const portsToTry = [SERVER_PORT, 5000, 5001, 5002, 5003, 5004, 5005];
    
    for (const port of portsToTry) {
        try {
            const response = await fetch(`${SERVER_HOST}:${port}/status`, {
                method: 'GET',
                timeout: 2000
            });
              if (response.ok) {
                SERVER_PORT = port;
                updateServerStatus('online', `Server Online (Port ${port})`);
                updateConnectionStatus('online');
                addMessage(`🟢 Connected to server! Now using advanced AI responses.`, 'bot');
                return true;
            }
        } catch (error) {
            // Try next port
        }
    }
      // If we get here, all ports failed
    updateServerStatus('offline', 'Offline Mode (Basic Responses)');
    updateConnectionStatus('offline');
    return false;
}

// Update server status indicator
function updateServerStatus(status, text) {
    const statusDot = document.getElementById('status-dot');
    const statusText = document.getElementById('status-text');
    
    statusDot.className = `status-dot ${status}`;
    statusText.textContent = text;
    
    // Update mode based on server status
    if (status === 'online') {
        isOfflineMode = false;
    } else {
        isOfflineMode = true;
    }
}

// Update connection status in header
function updateConnectionStatus(status) {
    const connectionDot = document.getElementById('connection-dot');
    connectionDot.className = `connection-dot ${status}`;
}

// Start server function
async function startServer() {
    const startBtn = document.getElementById('start-server-btn');
    const testBtn = document.getElementById('test-server-btn');
    
    startBtn.disabled = true;
    testBtn.disabled = true;
    updateServerStatus('testing', 'Starting Server...');
    
    try {        // Show instructions to user
        const instruction = `
        To enable advanced AI responses, please run this command in your terminal:
        
        cd "K:/My Drive/Study/old/8th/AI Lab/GreentBot"
        python simple_server.py
        
        Or click 'Try Server Connection' if server is already running.
        
        Note: The chatbot works in offline mode even without the server!
        `;
        
        alert(instruction);
        
        // Test if server is already running
        setTimeout(async () => {            const isOnline = await checkServerStatus();
            if (!isOnline) {
                updateServerStatus('offline', 'Offline Mode (Basic Responses)');
            }
            startBtn.disabled = false;
            testBtn.disabled = false;
        }, 2000);
        
    } catch (error) {
        console.error('Error starting server:', error);        updateServerStatus('offline', 'Offline Mode (Basic Responses)');
        startBtn.disabled = false;
        testBtn.disabled = false;
    }
}

// Test server connection
async function testServer() {
    const testBtn = document.getElementById('test-server-btn');
    testBtn.disabled = true;
    updateServerStatus('testing', 'Testing Connection...');
    
    const isOnline = await checkServerStatus();
    
    if (isOnline) {
        // Test chat API
        try {
            const response = await fetch(`${SERVER_HOST}:${SERVER_PORT}/api/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: 'Hello' })
            });
            
            if (response.ok) {
                const data = await response.json();
                addMessage('✅ Server connection test successful!', 'bot');
                addMessage(`Test response: ${data.response}`, 'bot');
                addMessage(`Connected to server at ${SERVER_HOST}:${SERVER_PORT}`, 'bot');
            }
        } catch (error) {
            addMessage('❌ Chat API test failed', 'bot');
        }    } else {
        addMessage('❌ Cannot connect to server. Continuing in offline mode with basic responses.', 'bot');
        addMessage('💡 Tip: The chatbot works offline! For advanced AI responses, start the Python server and click "Try Server Connection".', 'bot');
    }
    
    testBtn.disabled = false;
}

// Start periodic server checking
function startServerMonitoring() {
    // Set initial offline status
    updateServerStatus('testing', 'Checking for Server...');
    updateConnectionStatus('offline');
    
    // Check immediately for server
    checkServerStatus();
    
    // Check every 10 seconds (more frequent during auto-start)
    serverCheckInterval = setInterval(checkServerStatus, 10000);
}

// Automatic server startup function
async function attemptAutoServerStart() {
    console.log("Attempting automatic server startup...");
    
    // First check if server is already running
    const isAlreadyRunning = await checkServerStatus();
    if (isAlreadyRunning) {
        addMessage("🟢 Server is already running! You're now using advanced AI responses.", 'bot');
        return;
    }
    
    // Try to start server automatically using different methods
    addMessage("🚀 Attempting to start server automatically...", 'bot');
    
    try {
        // Method 1: Try to execute the restart script via file protocol
        const scriptCommands = [
            'python simple_server.py',
            '.\\restart_server.bat',
            'powershell .\\restart_server.ps1',
            'python ..\\simple_server.py'
        ];
        
        // Since we can't directly execute system commands from browser,
        // we'll try to detect if the server starts by checking periodically
        let attempts = 0;
        const maxAttempts = 20; // Check for 20 seconds
        
        const autoStartInterval = setInterval(async () => {
            attempts++;
            console.log(`Auto-start check attempt ${attempts}/${maxAttempts}`);
            
            const serverOnline = await checkServerStatus();
            if (serverOnline) {
                clearInterval(autoStartInterval);
                addMessage("✅ Server started successfully! Now using advanced AI responses.", 'bot');
                return;
            }
              if (attempts >= maxAttempts) {
                clearInterval(autoStartInterval);
                addMessage("⚠️ Automatic server startup not detected. Using offline mode with basic responses.", 'bot');
                addMessage("🎯 For advanced AI responses, you have these options:", 'bot');
                addMessage("1️⃣ Double-click 'auto-start-server.bat' in the react-chatbot folder", 'bot');
                addMessage("2️⃣ Click 'Start Server' button below and follow instructions", 'bot');
                addMessage("3️⃣ The chatbot works great in offline mode too! 😊", 'bot');
            }
        }, 1000); // Check every second
        
    } catch (error) {
        console.error('Auto-start error:', error);
        addMessage("⚠️ Could not auto-start server. Using offline mode.", 'bot');
        addMessage("💡 Click \"Start Server\" button below for manual setup instructions.", 'bot');
    }
}

// Initialize server monitoring when page loads
document.addEventListener('DOMContentLoaded', function() {
    startServerMonitoring();
});
