@echo off
echo Starting Green University Chatbot...
echo.
echo Starting HTTP server on port 8000...
start /min python -m http.server 8000

echo Waiting for server to start...
timeout /t 3 /nobreak >nul

echo Opening chatbot in browser...
start http://localhost:8000

echo.
echo Chatbot is now running at: http://localhost:8000
echo To stop the server, close the command prompt window or press Ctrl+C
echo.
pause
