Write-Host "Starting Green University Chatbot..." -ForegroundColor Green
Write-Host ""

# Change to the react-chatbot directory
Set-Location -Path "d:\VS Code\GreentBot\react-chatbot"

Write-Host "Starting HTTP server on port 8000..." -ForegroundColor Yellow
Start-Process python -ArgumentList "-m", "http.server", "8000" -WindowStyle Minimized

Write-Host "Waiting for server to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "Opening chatbot in browser..." -ForegroundColor Yellow
Start-Process "http://localhost:8000"

Write-Host ""
Write-Host "Chatbot is now running at: http://localhost:8000" -ForegroundColor Green
Write-Host "To stop the server, close the Python process or press Ctrl+C in the server window" -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to exit"
