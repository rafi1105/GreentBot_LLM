# Auto-start Green University Chatbot Server
Write-Host "🚀 Auto-starting Green University Chatbot Server..." -ForegroundColor Green

# Change to parent directory (where simple_server.py is located)
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$parentPath = Split-Path -Parent $scriptPath
Set-Location $parentPath

Write-Host "📂 Changed to directory: $parentPath" -ForegroundColor Cyan

# Kill any existing processes on port 5000
Write-Host "🔍 Checking for existing server processes..." -ForegroundColor Yellow
try {
    $processes = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | 
                 Where-Object {$_.State -eq "Listen"} | 
                 Select-Object -ExpandProperty OwningProcess

    foreach ($processId in $processes) {
        try {
            $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
            if ($process) {
                Write-Host "⚠️  Stopping existing server process $processId..." -ForegroundColor Red
                Stop-Process -Id $processId -Force
            }
        } catch {
            Write-Host "⚠️  Could not stop process $processId" -ForegroundColor Red
        }
    }
} catch {
    Write-Host "ℹ️  No existing processes found on port 5000" -ForegroundColor Gray
}

# Start the server
Write-Host "🎯 Starting server..." -ForegroundColor Green
try {
    Start-Process -FilePath "python" -ArgumentList "simple_server.py" -WindowStyle Minimized
    Write-Host "✅ Server startup initiated successfully!" -ForegroundColor Green
    Write-Host "🌐 Check the web interface for connection status." -ForegroundColor Cyan
    Write-Host "📱 Open index.html in your browser to use the chatbot." -ForegroundColor Yellow
} catch {
    Write-Host "❌ Failed to start server. Please check if Python is installed and simple_server.py exists." -ForegroundColor Red
    Write-Host "💡 You can still use the chatbot in offline mode!" -ForegroundColor Green
}

# Wait a moment then exit
Start-Sleep -Seconds 3
Write-Host "✨ Auto-start complete. Happy chatting!" -ForegroundColor Magenta
