## Running Your Chatbot Web Interface

### Prerequisites
- Python 3.6 or higher
- Flask and Flask-CORS installed
- Windows 10 or later

### Setup Instructions (Windows)

1. Open a Command Prompt or PowerShell window

2. Install the required Python libraries:
   ```
   pip install flask flask-cors
   ```

3. Run the Flask backend server:
   ```
   cd "K:\My Drive\Study\old\8th\AI Lab\GreentBot"
   python app.py
   ```
   
4. Open the web interface by opening the file:
   ```
   K:\My Drive\Study\old\8th\AI Lab\GreentBot\react-chatbot\index.html
   ```
   
   You can open this file directly in your web browser.

### Troubleshooting

If you see error messages:

1. Make sure Flask and Flask-CORS are installed:
   ```
   pip install flask flask-cors
   ```

2. Make sure the Flask server is running and shows:
   ```
   * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
   ```

3. If you see import errors, check that your Python environment has all the required packages:
   ```
   pip install flask flask-cors numpy scikit-learn nltk
   ```

4. Try a different browser if the web interface doesn't connect to the server.

### Web Interface Files

- `react-chatbot/index.html` - The main chatbot interface
- `react-chatbot/styles.css` - Styling for the chatbot
- `react-chatbot/script.js` - JavaScript that connects to the Flask API

### How It Works

1. The Flask backend exposes your chatbot's functionality as an API
2. The web interface sends user messages to the API
3. The API processes the message using your existing chatbot logic
4. The response is returned to the web interface and displayed
