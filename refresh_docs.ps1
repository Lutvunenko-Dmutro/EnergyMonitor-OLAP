# 🚀 Скрипт повного оновлення документації Atlas
$env:DISABLE_MKDOCS_2_WARNING = "true"
Write-Host "--- Починаю повну синхронізацію Atlas ---" -ForegroundColor Cyan

# 1. Генерація метаданих та ін'єкція в Атлас
Write-Host "[1/2] Оновлення метаданих та JSON..." -ForegroundColor Yellow
python scripts/system/generate_atlas_metadata.py
python scripts/generate_atlas_metadata.py

# 2. Повна збірка сайту
Write-Host "[2/2] Перезбірка статичного сайту ProperDocs..." -ForegroundColor Yellow
$properdocs = "$env:LOCALAPPDATA\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts\properdocs.exe"
if (Test-Path $properdocs) {
    & $properdocs build --clean
} else {
    python -m mkdocs build --clean
}

Write-Host "✅ Все готово! Тепер Atlas актуальний." -ForegroundColor Green
Write-Host "Якщо запущено 'properdocs serve', зміни підтягнуться автоматично." -ForegroundColor Cyan
