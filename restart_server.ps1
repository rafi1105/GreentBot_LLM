# Kill any existing Python processes running on port 5000
Write-Host "Stopping any existing Python servers on port 5000..." -ForegroundColor Yellow
$processes = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | 
             Where-Object {$_.State -eq "Listen"} | 
             Select-Object -ExpandProperty OwningProcess

foreach ($processId in $processes) {
    try {
        $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
        if ($process) {
            Write-Host "Killing process $processId..." -ForegroundColor Cyan
            Stop-Process -Id $processId -Force
        }
    } catch {
        Write-Host "Error stopping process: $_" -ForegroundColor Red
    }
}

# Start the server
Write-Host "Starting Green University Chatbot Server..." -ForegroundColor Green
python simple_server.py
