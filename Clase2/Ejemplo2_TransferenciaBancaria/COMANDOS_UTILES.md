# 🔧 Comandos Útiles - API Transferencias Bancarias

## 📋 Tabla de Comandos Rápidos

### 🚀 Iniciar y Detener API

```powershell
# Iniciar API (modo normal)
python main.py

# Iniciar con reload automático (desarrollo)
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Iniciar en puerto diferente
python -m uvicorn main:app --port 8001

# Detener todos los procesos Python
Get-Process -Name python | Stop-Process -Force

# Iniciar en background (Job)
Start-Job -ScriptBlock { 
    Set-Location "C:\ruta\al\proyecto"
    python -m uvicorn main:app --host 0.0.0.0 --port 8000 
}

# Ver jobs en ejecución
Get-Job

# Detener job específico
Stop-Job -Id 1
Remove-Job -Id 1
```

---

## 🧪 Ejecutar Tests

```powershell
# Suite completa - básico
$env:AUTH_TOKEN="Bearer test"
pytest -v

# Suite completa con reportes HTML
$env:AUTH_TOKEN="Bearer test"
pytest --cov=main --cov-report=html --html=report.html --self-contained-html -v

# Solo tests que pasaron
pytest -v --tb=no

# Solo tests fallidos
pytest -v --lf

# Test específico
pytest tests/test_transferencias.py::test_01_transferencia_exitosa_path_feliz -v

# Con output detallado
pytest -vv -s

# Modo quiet (solo resumen)
pytest -q

# Ejecutar N veces (stress test)
pytest --count=10 -v

# Ejecutar en paralelo (requiere pytest-xdist)
# pip install pytest-xdist
pytest -n 4 -v
```

---

## 🌐 Probar API con curl/Invoke-WebRequest

### Health Check
```powershell
# Con curl (alias de Invoke-WebRequest)
curl http://localhost:8000/health

# Con Invoke-WebRequest
Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing | Select-Object StatusCode, Content
```

### Transferencia Exitosa
```powershell
$body = @{
    origen = "12345678"
    destino = "87654321"
    monto = 1000
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/transferencias" `
    -Method POST `
    -Body $body `
    -Headers @{
        "Content-Type" = "application/json"
        "Authorization" = "Bearer test"
    } `
    -UseBasicParsing | Select-Object StatusCode, Content
```

### Transferencia con OTP
```powershell
$body = @{
    origen = "12345678"
    destino = "87654321"
    monto = 2000000
    otp = "123456"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/transferencias" `
    -Method POST `
    -Body $body `
    -Headers @{
        "Content-Type" = "application/json"
        "Authorization" = "Bearer test"
        "X-OTP" = "123456"
    } `
    -UseBasicParsing
```

### Obtener Historial
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/transferencias/historial" `
    -UseBasicParsing | ConvertFrom-Json
```

### Consultar Cuenta
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/cuentas/12345678" `
    -UseBasicParsing | ConvertFrom-Json
```

### Reset Cuenta
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/cuentas/12345678/reset" `
    -Method POST `
    -UseBasicParsing | ConvertFrom-Json
```

---

## 📊 Generar Reportes

```powershell
# Reporte HTML de tests
$env:AUTH_TOKEN="Bearer test"
pytest --html=report.html --self-contained-html

# Abrir reporte en navegador
Start-Process report.html

# Reporte de cobertura
$env:AUTH_TOKEN="Bearer test"
pytest --cov=main --cov-report=html

# Abrir cobertura en navegador
Start-Process htmlcov/index.html

# Reporte de cobertura en terminal
pytest --cov=main --cov-report=term-missing

# Exportar cobertura XML (para CI/CD)
pytest --cov=main --cov-report=xml

# Reportes combinados
pytest --cov=main --cov-report=html --cov-report=term --html=report.html --self-contained-html -v
```

---

## 🔍 Debugging

```powershell
# Ejecutar con debugger (pdb)
pytest --pdb

# Ejecutar con logs detallados
pytest --log-cli-level=DEBUG -v

# Ejecutar solo hasta primer fallo
pytest -x

# Mostrar 10 tests más lentos
pytest --durations=10

# Mostrar todas las variables locales en fallos
pytest -l

# Captura de stdout/stderr
pytest -s  # No capturar (mostrar prints)
pytest --capture=no  # Equivalente
```

---

## 🧹 Limpieza

```powershell
# Limpiar cache de pytest
Remove-Item -Recurse -Force .pytest_cache

# Limpiar reportes generados
Remove-Item -Force report.html
Remove-Item -Recurse -Force htmlcov
Remove-Item -Force .coverage

# Limpiar __pycache__
Get-ChildItem -Recurse -Filter __pycache__ | Remove-Item -Recurse -Force

# Limpiar todo
Remove-Item -Recurse -Force .pytest_cache, htmlcov, __pycache__
Remove-Item -Force report.html, .coverage
```

---

## 📦 Gestión de Dependencias

```powershell
# Instalar todas las dependencias
python -m pip install -r requirements.txt

# Instalar con upgrade
python -m pip install -r requirements.txt --upgrade

# Instalar en entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Generar requirements.txt actualizado
pip freeze > requirements.txt

# Verificar dependencias instaladas
pip list

# Buscar paquete específico
pip show pytest

# Desinstalar paquete
pip uninstall pytest -y
```

---

## 🔐 Variables de Entorno

```powershell
# Configurar múltiples variables
$env:BASE_URL = "http://localhost:8000"
$env:AUTH_TOKEN = "Bearer test_token_123"
$env:TRANSFER_ENDPOINT = "/api/transferencias"
$env:SRC_ACCOUNT = "12345678"
$env:DST_ACCOUNT = "87654321"

# Ver variable específica
echo $env:AUTH_TOKEN

# Ver todas las variables
Get-ChildItem Env:

# Limpiar variable
Remove-Item Env:AUTH_TOKEN

# Guardar en archivo .env (requiere python-dotenv)
@"
BASE_URL=http://localhost:8000
AUTH_TOKEN=Bearer test
"@ | Out-File .env -Encoding UTF8

# Cargar desde .env en Python
# from dotenv import load_dotenv
# load_dotenv()
```

---

## 📡 Postman CLI (Newman)

```powershell
# Instalar Newman (requiere Node.js)
npm install -g newman

# Ejecutar colección Postman
newman run Transferencias_Bancarias.postman_collection.json

# Con variables de entorno
newman run Transferencias_Bancarias.postman_collection.json `
    --env-var "base_url=http://localhost:8000" `
    --env-var "auth_token=Bearer test"

# Generar reporte HTML
newman run Transferencias_Bancarias.postman_collection.json `
    --reporters cli,html `
    --reporter-html-export newman-report.html

# Ejecutar con delays (para rate limiting)
newman run Transferencias_Bancarias.postman_collection.json `
    --delay-request 1000
```

---

## 🐳 Docker (Opcional)

```powershell
# Crear Dockerfile
@"
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
"@ | Out-File Dockerfile -Encoding UTF8

# Build imagen
docker build -t transferencias-api .

# Ejecutar contenedor
docker run -d -p 8000:8000 --name api-transferencias transferencias-api

# Ver logs
docker logs api-transferencias

# Detener y eliminar
docker stop api-transferencias
docker rm api-transferencias
```

---

## 📊 Monitoreo

```powershell
# Ver uso de CPU/memoria del proceso Python
Get-Process python | Select-Object CPU, WorkingSet, ProcessName

# Monitorear en tiempo real (requiere loop)
while ($true) {
    Clear-Host
    Get-Process python | Format-Table CPU, WS, ProcessName -AutoSize
    Start-Sleep -Seconds 2
}

# Verificar puerto en uso
netstat -ano | findstr :8000

# Ver conexiones activas
Get-NetTCPConnection -LocalPort 8000
```

---

## 🎯 Shortcuts Útiles

```powershell
# Alias personalizados (agregar a $PROFILE)
function Start-API { python main.py }
function Run-Tests { $env:AUTH_TOKEN="Bearer test"; pytest -v }
function Run-TestsReport { 
    $env:AUTH_TOKEN="Bearer test"
    pytest --cov=main --cov-report=html --html=report.html --self-contained-html -v
    Start-Process report.html
}

# Usar aliases
Start-API
Run-Tests
Run-TestsReport
```

---

## 📝 Logs y Auditoría

```powershell
# Redirigir output de API a archivo
python main.py > api.log 2>&1

# Ver log en tiempo real (tail -f equivalent)
Get-Content api.log -Wait

# Buscar en logs
Select-String -Path api.log -Pattern "ERROR"

# Filtrar logs por timestamp
Get-Content api.log | Where-Object { $_ -match "2025-12-10" }
```

---

**Tip**: Guardar estos comandos en un script `comandos.ps1` para acceso rápido.
