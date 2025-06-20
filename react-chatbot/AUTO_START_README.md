# Green University Chatbot - Auto Start Guide

## 🚀 Quick Start Options

### Option 1: Automatic Server Startup (Easiest)
1. **Double-click** `auto-start-server.bat` in the `react-chatbot` folder
2. Open `index.html` in your browser
3. The chatbot will automatically detect and connect to the server

### Option 2: Manual Server Start
1. Open Command Prompt or PowerShell
2. Navigate to the project folder:
   ```
   cd "K:/My Drive/Study/old/8th/AI Lab/GreentBot"
   ```
3. Run the server:
   ```
   python simple_server.py
   ```
4. Open `index.html` in your browser

### Option 3: Offline Mode Only
- Simply open `index.html` or `standalone.html`
- The chatbot works immediately with basic responses
- No server setup required!

## 📁 File Structure
- `index.html` - Main chatbot interface with server auto-detection
- `standalone.html` - Pure offline version (no server features)
- `auto-start-server.bat` - One-click server startup
- `script.js` - Main chatbot logic with auto-start feature
- `offline-chatbot.js` - Offline response engine

## 🔧 How Auto-Start Works
1. When you open `index.html`, it automatically checks for a running server
2. If no server is found, it provides clear instructions
3. The `auto-start-server.bat` file handles server startup automatically
4. The interface seamlessly switches between offline and online modes

## 💡 Tips
- The auto-start feature checks for the server every 10 seconds
- You'll see status updates in the chat and in the bottom panel
- Green dot = Server connected, Red dot = Offline mode
- Both modes work great - server mode just has more advanced AI responses!

## 🆘 Troubleshooting
- If auto-start doesn't work, try running `auto-start-server.bat` as administrator
- Check that Python is installed and accessible from command line
- Port 5000 conflicts? The server automatically finds an available port
- Still having issues? The offline mode provides excellent basic responses!
