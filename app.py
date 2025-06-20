from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
from chatbotgui import find_best_match

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing to allow requests from any origin

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_input = data.get('message', '')
        
        if not user_input or not isinstance(user_input, str):
            return jsonify({'response': 'Please enter a valid question.'}), 400
        
        # Use the chatbot's existing find_best_match function
        response = find_best_match(user_input)
        
        # Ensure we have a valid response
        if not response or not isinstance(response, str):
            response = "I'm sorry, I couldn't process that request."
        
        print(f"User input: {user_input}")
        print(f"Bot response: {response}")
        
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'response': f"I'm sorry, an error occurred: {str(e)}"}), 500

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chatbot API</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
            pre { background: #f8f8f8; padding: 10px; border-radius: 5px; overflow-x: auto; }
        </style>
    </head>
    <body>
        <h1>Green University Chatbot API</h1>
        <p>Your chatbot API is running successfully!</p>
        <h2>How to use:</h2>
        <ol>
            <li>Make sure this server is running</li>
            <li>Open <code>react-chatbot/index.html</code> in your browser</li>
            <li>Start chatting with the bot</li>
        </ol>
        <h2>API Endpoint:</h2>
        <pre>POST /api/chat
Content-Type: application/json

{
    "message": "Your question here"
}</pre>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("Starting Flask server for GreenBot...")
    print("Open react-chatbot/index.html in your browser to chat with the bot")
    app.run(debug=True, port=5000)
