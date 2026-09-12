$ErrorActionPreference = "Continue"

Write-Host "Starting Ollama (if not running)..."
$ollama = Get-Process ollama -ErrorAction SilentlyContinue
if (-not $ollama) {
    Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 5
} else {
    Write-Host "Ollama already running."
}

Write-Host "Starting AarogyaSathi server on http://127.0.0.1:8000 ..."
$env:PYTHONPATH = "$PWD"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
