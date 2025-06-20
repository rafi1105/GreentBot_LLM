@echo off
title Green University Chatbot Server
echo.
echo ================================================
echo    🤖 Green University Chatbot Server
echo ================================================
echo.
echo Starting server...
echo.

cd /d "K:\My Drive\Study\old\8th\AI Lab\GreentBot"

if not exist ".venv\Scripts\python.exe" (
    echo ❌ Virtual environment not found!
    echo Please make sure the virtual environment is set up properly.
    pause
    exit /b 1
)

echo ✅ Virtual environment found
echo 🚀 Starting chatbot server...
echo.

".venv\Scripts\python.exe" simple_server.py

echo.
echo Server stopped.
pause
