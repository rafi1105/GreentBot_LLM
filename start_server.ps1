# Green University Chatbot Server Launcher
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   🤖 Green University Chatbot Server" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$projectPath = "K:\My Drive\Study\old\8th\AI Lab\GreentBot"
$pythonPath = "$projectPath\.venv\Scripts\python.exe"
$serverScript = "$projectPath\simple_server.py"

Write-Host "📁 Changing to project directory..." -ForegroundColor Yellow
Set-Location $projectPath

if (-not (Test-Path $pythonPath)) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please make sure the virtual environment is set up properly." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Virtual environment found" -ForegroundColor Green
Write-Host "🚀 Starting chatbot server..." -ForegroundColor Green
Write-Host ""
Write-Host "💡 Once the server starts, open: http://localhost:5000" -ForegroundColor Yellow
Write-Host "💬 Or use the chatbot at: react-chatbot/index.html" -ForegroundColor Yellow
Write-Host ""
Write-Host "⏹️  Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

try {
    & $pythonPath $serverScript
} catch {
    Write-Host "❌ Error starting server: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
}
