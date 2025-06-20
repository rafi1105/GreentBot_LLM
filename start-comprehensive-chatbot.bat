@echo off
echo ============================================================
echo  GREEN UNIVERSITY CHATBOT - COMPREHENSIVE ML SYSTEM
echo ============================================================
echo.

echo 🔧 Installing Python dependencies...
pip install -r requirements_comprehensive.txt

echo.
echo 🚀 Starting Comprehensive ML API Server...
start /min python api_server.py

echo.
echo ⏳ Waiting for API server to start...
timeout /t 5 /nobreak >nul

echo.
echo 🌐 Starting Web Server...
cd react-chatbot
start /min python -m http.server 8000

echo.
echo ⏳ Waiting for web server to start...
timeout /t 3 /nobreak >nul

echo.
echo 🌍 Opening Comprehensive Chatbot in browser...
start http://localhost:8000

echo.
echo ============================================================
echo ✅ COMPREHENSIVE ML CHATBOT IS NOW RUNNING!
echo ============================================================
echo.
echo 🤖 Features:
echo    • Analyzes ALL JSON data before responding
echo    • Uses supervised learning for category prediction  
echo    • Enhanced keyword and semantic matching
echo    • Confidence scoring and detailed analytics
echo.
echo 🌐 Web Interface: http://localhost:8000
echo 📡 API Server: http://localhost:5000
echo 📖 API Docs: http://localhost:5000
echo.
echo Press any key to stop all servers...
pause >nul

echo.
echo 🛑 Stopping servers...
taskkill /f /im python.exe >nul 2>&1
echo Done!
pause
