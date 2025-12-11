# Script para iniciar la API de transferencias
Write-Host "Iniciando API de Transferencias Bancarias..." -ForegroundColor Green
python -m pip install -q -r requirements.txt
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
