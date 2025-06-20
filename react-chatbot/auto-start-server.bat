@echo off
echo Auto-starting Green University Chatbot Server...
cd /d "%~dp0\.."

REM Kill any existing processes on port 5000
echo Checking for existing server processes...
for /f "tokens=5" %%p in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
    if not "%%p"=="" (
        echo Stopping existing server process %%p...
        taskkill /F /PID %%p 2>nul
    )
)

echo Starting server...
start /min python simple_server.py

echo Server startup initiated. Check the web interface for connection status.
timeout /t 3 /nobreak >nul
exit
