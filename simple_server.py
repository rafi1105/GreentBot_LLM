#!/usr/bin/env python3
"""
Simple Flask server for the Green University Chatbot
"""

import sys
import json
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver
import urllib.parse as urlparse
from urllib.parse import parse_qs
import threading
import time

# Try to import our chatbot
try:
    from chatbotgui import find_best_match
    print("✓ Chatbot module loaded successfully")
except ImportError as e:
    print(f"✗ Error importing chatbot: {e}")
    def find_best_match(query):
        return "Sorry, the chatbot module is not available."

class ChatbotHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/chat':
            # Handle chat API
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                user_message = data.get('message', '')
                print(f"User: {user_message}")
                
                # Get response from chatbot
                response = find_best_match(user_message)
                print(f"Bot: {response}")
                
                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
                
                response_data = json.dumps({'response': response})
                self.wfile.write(response_data.encode('utf-8'))
                
            except Exception as e:
                print(f"Error processing request: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = json.dumps({'response': f'Server error: {str(e)}'})
                self.wfile.write(error_response.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        if self.path == '/' or self.path == '/status':
            # Server status page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Green University Chatbot Server</title>
                <style>
                    body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                    .status { background: #e8f5e8; padding: 20px; border-radius: 5px; margin: 20px 0; }
                    .endpoint { background: #f0f0f0; padding: 10px; border-radius: 3px; font-family: monospace; }
                </style>
            </head>
            <body>
                <h1>🤖 Green University Chatbot Server</h1>
                <div class="status">
                    <h2>✅ Server Status: RUNNING</h2>
                    <p><strong>Port:</strong> 5000</p>
                    <p><strong>Chat API Endpoint:</strong></p>
                    <div class="endpoint">POST http://localhost:5000/api/chat</div>
                </div>
                
                <h3>How to use:</h3>
                <ol>
                    <li>Keep this server running</li>
                    <li>Open <code>react-chatbot/index.html</code> in your browser</li>
                    <li>Start chatting with the Green University Bot!</li>
                </ol>
                
                <h3>Test the API:</h3>
                <button onclick="testAPI()">Test Chat API</button>
                <div id="test-result"></div>
                
                <script>
                function testAPI() {
                    fetch('/api/chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({message: 'Hello'})
                    })
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('test-result').innerHTML = 
                            '<p><strong>Test Result:</strong> ' + data.response + '</p>';
                    })
                    .catch(error => {
                        document.getElementById('test-result').innerHTML = 
                            '<p style="color:red;"><strong>Error:</strong> ' + error + '</p>';
                    });
                }
                </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def find_available_port(start_port=5000, max_port=5050):
    """Find an available port starting from start_port up to max_port"""
    for port in range(start_port, max_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(('', port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"Could not find an available port between {start_port} and {max_port}")

def start_server():
    try:
        PORT = find_available_port()
        
        # Update HTML status with actual port
        ChatbotHTTPRequestHandler.do_GET = lambda self, *args, **kwargs: handle_get(self, PORT)
        
        with socketserver.TCPServer(("", PORT), ChatbotHTTPRequestHandler) as httpd:
            print(f"\n🚀 Green University Chatbot Server Starting...")
            print(f"📡 Server running at: http://localhost:{PORT}")
            print(f"💬 Chat API available at: http://localhost:{PORT}/api/chat")
            print(f"📁 Open react-chatbot/index.html in your browser to chat!")
            print(f"⏹️  Press Ctrl+C to stop the server\n")
            
            # Create a file to store the port for the UI to read
            with open("server_port.txt", "w") as f:
                f.write(str(PORT))
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

def handle_get(self, port):
    if self.path == '/' or self.path == '/status':
        # Server status page
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Green University Chatbot Server</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }}
                .status {{ background: #e8f5e8; padding: 20px; border-radius: 5px; margin: 20px 0; }}
                .endpoint {{ background: #f0f0f0; padding: 10px; border-radius: 3px; font-family: monospace; }}
            </style>
        </head>
        <body>
            <h1>🤖 Green University Chatbot Server</h1>
            <div class="status">
                <h2>✅ Server Status: RUNNING</h2>
                <p><strong>Port:</strong> {port}</p>
                <p><strong>Chat API Endpoint:</strong></p>
                <div class="endpoint">POST http://localhost:{port}/api/chat</div>
            </div>
            
            <h3>How to use:</h3>
            <ol>
                <li>Keep this server running</li>
                <li>Open <code>react-chatbot/index.html</code> in your browser</li>
                <li>Start chatting with the Green University Bot!</li>
            </ol>
            
            <h3>Test the API:</h3>
            <button onclick="testAPI()">Test Chat API</button>
            <div id="test-result"></div>
            
            <script>
            function testAPI() {{
                fetch('/api/chat', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{message: 'Hello'}})
                }})
                .then(response => response.json())
                .then(data => {{
                    document.getElementById('test-result').innerHTML = 
                        '<p><strong>Test Result:</strong> ' + data.response + '</p>';
                }})
                .catch(error => {{
                    document.getElementById('test-result').innerHTML = 
                        '<p style="color:red;"><strong>Error:</strong> ' + error + '</p>';
                }});
            }}
            </script>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))
    else:
        self.send_response(404)
        self.end_headers()

if __name__ == "__main__":
    start_server()
