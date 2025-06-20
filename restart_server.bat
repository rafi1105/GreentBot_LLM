@echo off
echo Stopping any existing Python servers on port 5000...
for /f "tokens=5" %%p in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
    if not "%%p"=="" (
        echo Killing process %%p...
        taskkill /F /PID %%p 2>nul
    )
)

echo Starting Green University Chatbot Server...
echo.
python simple_server.py
