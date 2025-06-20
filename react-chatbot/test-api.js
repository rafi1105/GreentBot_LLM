// Simple test script to debug chatbot communication
const testApiCall = async () => {
    console.log("Testing API call to the chatbot server...");
    
    try {
        const response = await fetch('http://localhost:5000/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: "hello" }),
            cache: 'no-cache'
        });
        
        console.log("Response status:", response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log("Response data:", data);
        
        if (data && data.response) {
            console.log("Chatbot response:", data.response);
            document.body.innerHTML = `<h2>Test successful!</h2>
                <p>Server responded with: "${data.response}"</p>
                <p>The server is working correctly. Please return to the main chat interface.</p>
                <button onclick="window.location.href='index.html'">Back to Chat</button>`;
        } else {
            console.error("No response data found");
            document.body.innerHTML = `<h2>Test failed!</h2>
                <p>No response data received from server.</p>
                <p>Check browser console for more details.</p>`;
        }
    } catch (error) {
        console.error("Error testing API:", error);
        document.body.innerHTML = `<h2>Test failed!</h2>
            <p>Error: ${error.message}</p>
            <p>Make sure the Flask server is running at http://localhost:5000</p>`;
    }
};

// Call the test function when the page loads
window.onload = testApiCall;
