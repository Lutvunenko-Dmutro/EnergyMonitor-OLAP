# 🛡️ ENERGY MONITOR - Project Atlas Starter (Modern Edition)
$ErrorActionPreference = "Continue"
$Host.UI.RawUI.WindowTitle = "🛡️ ENERGY MONITOR - Project Atlas"

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "   🚀 Starting Energy Monitor Documentation System" -ForegroundColor Cyan
Write-Host "   (Using ProperDocs Defense Edition)" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Синхронізація метаданих
Write-Host "[1/2] Synchronizing Atlas metadata..." -ForegroundColor Yellow
powershell -ExecutionPolicy Bypass -File refresh_docs.ps1

Write-Host ""

# 2. Запуск сервера ProperDocs
Write-Host "[2/2] Starting local server at http://127.0.0.1:8000" -ForegroundColor Yellow
$properdocs = "$env:LOCALAPPDATA\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts\properdocs.exe"

if (Test-Path $properdocs) {
    & $properdocs serve
} else {
    python -m mkdocs serve
}

Read-Host -Prompt "Натисніть Enter, щоб закрити вікно"
