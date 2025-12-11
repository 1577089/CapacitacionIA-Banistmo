# 🚀 GUÍA DE EJECUCIÓN - Automatización de Tests

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Instalación y Configuración](#instalación-y-configuración)
3. [Ejecución de la Automatización](#ejecución-de-la-automatización)
4. [Verificación de Resultados](#verificación-de-resultados)
5. [Resolución de Problemas](#resolución-de-problemas)
6. [Configuración Avanzada](#configuración-avanzada)

---

## 📦 Requisitos Previos

### Software Necesario

| Software | Versión Mínima | Verificación | Instalación |
|----------|----------------|--------------|-------------|
| **Python** | 3.8+ | `python --version` | [python.org](https://www.python.org/downloads/) |
| **pip** | 20.0+ | `pip --version` | Incluido con Python |
| **PowerShell** | 5.1+ | `$PSVersionTable.PSVersion` | Incluido en Windows |
| **Git** (opcional) | 2.0+ | `git --version` | [git-scm.com](https://git-scm.com/) |

### Verificar Python

```powershell
# Verificar versión de Python
python --version
# Salida esperada: Python 3.8.x o superior

# Verificar pip
pip --version
# Salida esperada: pip 20.0.x o superior
```

**Si Python no está instalado:**
1. Descargar de https://www.python.org/downloads/
2. Durante instalación, marcar "Add Python to PATH"
3. Reiniciar PowerShell
4. Verificar instalación con `python --version`

---

## ⚙️ Instalación y Configuración

### Paso 1: Navegar al Directorio del Proyecto

```powershell
# Abrir PowerShell y navegar al proyecto
cd "C:\Users\1577089\Desktop\CapacitacionIA-Banistmo\CapacitacionIA-Banistmo\Clase2\Ejemplo2_TransferenciaBancaria"

# Verificar que estás en el directorio correcto
Get-Location
```

### Paso 2: Instalar Dependencias Python

```powershell
# Instalar todas las dependencias del proyecto
python -m pip install -r requirements.txt

# Salida esperada:
# - Successfully installed pytest-9.0.2
# - Successfully installed fastapi-0.115.x
# - Successfully installed uvicorn-0.x.x
# - Successfully installed pytest-cov-7.0.0
# - Successfully installed pytest-html-4.1.1
# - Successfully installed requests-2.x.x
# - Successfully installed pydantic-2.x.x
```

**Dependencias incluidas en `requirements.txt`:**
- `pytest` - Framework de testing
- `pytest-cov` - Cobertura de código
- `pytest-html` - Reportes HTML
- `requests` - Cliente HTTP para tests
- `fastapi` - Framework web API
- `uvicorn[standard]` - Servidor ASGI
- `pydantic` - Validación de datos

### Paso 3: Verificar Instalación

```powershell
# Verificar que pytest está instalado
pytest --version
# Salida esperada: pytest 9.0.2

# Verificar que FastAPI está instalado
python -c "import fastapi; print(f'FastAPI {fastapi.__version__}')"
# Salida esperada: FastAPI 0.115.x
```

### Paso 4: Configurar Variables de Entorno

```powershell
# Configurar token de autenticación
$env:AUTH_TOKEN = "Bearer test"

# Verificar configuración
echo $env:AUTH_TOKEN
# Salida esperada: Bearer test
```

**Variables de entorno disponibles:**

| Variable | Valor por Defecto | Descripción |
|----------|-------------------|-------------|
| `AUTH_TOKEN` | `"Bearer test"` | Token de autenticación para API |
| `BASE_URL` | `http://localhost:8000` | URL base de la API |
| `FORCE_MAINTENANCE` | No definido | Forzar modo mantenimiento (1=activado) |
| `BLOCKED_ACCOUNT` | No definido | ID de cuenta bloqueada para test |

---

## 🚀 Ejecución de la Automatización

### Método 1: Script Automatizado Completo (RECOMENDADO)

Este método ejecuta la API + Tests + Reportes SVE automáticamente.

```powershell
# Ejecutar tests con reportes SVE
.\run_tests_sve.ps1
```

**¿Qué hace este script?**
1. ✅ Configura variables de entorno automáticamente
2. ✅ Limpia reportes anteriores
3. ✅ Ejecuta la suite completa de 15 tests
4. ✅ Genera 3 formatos de reportes SVE (XML, JSON, CSV)
5. ✅ Muestra resumen de resultados

**Salida esperada:**
```
=============================================
  TESTS AUTOMATIZADOS + REPORTES SVE
=============================================

[OK] Variables de entorno configuradas

Ejecutando suite de tests...
=============================================

13 passed, 2 skipped in 78.33s

=============================================
[OK] TESTS COMPLETADOS EXITOSAMENTE

Verificando reportes SVE generados:
=============================================
   [OK] sve_report.xml - 8316 bytes
   [OK] sve_report.json - 8183 bytes
   [OK] sve_report.csv - 2883 bytes
```

### Método 2: Ejecución Manual Paso a Paso

#### Paso 2.1: Iniciar la API

**Terminal 1 - Iniciar servidor API:**
```powershell
# Iniciar la API FastAPI
python main.py

# Salida esperada:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete.
```

**Verificar que la API está funcionando:**
```powershell
# En otra terminal, verificar health endpoint
curl http://localhost:8000/health

# Salida esperada:
# {"status":"healthy","timestamp":"2025-12-10T..."}
```

#### Paso 2.2: Ejecutar Tests

**Terminal 2 - Ejecutar tests:**
```powershell
# Configurar token
$env:AUTH_TOKEN = "Bearer test"

# Ejecutar tests
pytest -v

# Salida esperada:
# 13 passed, 2 skipped in 78.33s
```

**Con reportes HTML:**
```powershell
pytest -v --html=report.html --self-contained-html
```

**Con cobertura de código:**
```powershell
pytest -v --cov=main --cov-report=html
```

### Método 3: Ejecutar Tests Específicos

```powershell
# Ejecutar solo un test específico
pytest -v tests/test_transferencias.py::test_01_transferencia_exitosa_path_feliz

# Ejecutar tests que coincidan con un patrón
pytest -v -k "limite"
# Ejecuta: test_02_excede_limite_diario, test_03_excede_limite_mensual

# Ejecutar tests con verbose y mostrar prints
pytest -v -s

# Ejecutar tests y detenerse en el primer fallo
pytest -v -x
```

### Método 4: Scripts PowerShell Individuales

```powershell
# Solo iniciar API
.\run_api.ps1

# Solo ejecutar tests (requiere API corriendo)
.\run_tests.ps1

# Tests + Reportes SVE
.\run_tests_sve.ps1
```

---

## 📊 Verificación de Resultados

### Archivos Generados

Después de ejecutar los tests, verifica que se generaron estos archivos:

```powershell
# Listar todos los archivos de reportes
Get-ChildItem | Where-Object { $_.Name -like "*report*" -or $_.Name -like "sve_*" }
```

**Archivos esperados:**

| Archivo | Descripción |
|---------|-------------|
| `report.html` | Reporte HTML visual de pytest |
| `htmlcov/index.html` | Reporte de cobertura de código |
| `sve_report.xml` | Reporte SVE formato XML |
| `sve_report.json` | Reporte SVE formato JSON |
| `sve_report.csv` | Reporte SVE formato CSV |
| `.coverage` | Datos de cobertura (binario) |

### Abrir Reportes

```powershell
# Abrir reporte HTML en navegador
start report.html

# Abrir reporte de cobertura
start htmlcov/index.html

# Abrir SVE JSON en VS Code
code sve_report.json

# Abrir SVE CSV en Excel
start sve_report.csv

# Ver SVE XML en notepad
notepad sve_report.xml
```

### Verificar Métricas de Calidad

```powershell
# Parsear JSON para ver métricas
$report = Get-Content sve_report.json | ConvertFrom-Json
Write-Host "Total Tests: $($report.summary.total_tests)"
Write-Host "Passed: $($report.summary.passed)"
Write-Host "Failed: $($report.summary.failed)"
Write-Host "Pass Rate: $($report.summary.pass_rate)"
```

**Métricas esperadas:**
- ✅ Total Tests: 15
- ✅ Passed: 13
- ✅ Failed: 0
- ✅ Skipped: 2
- ✅ Pass Rate: 86.67%

### Verificar Tests Individuales

```powershell
# Ver lista de tests ejecutados
pytest --collect-only

# Ver resultados del último run
pytest --last-failed --verbose

# Ver tests más lentos
pytest --durations=10
```

---

## 🔧 Configuración Avanzada

### Tests con Condiciones Especiales

#### Test 06: Horario de Mantenimiento

```powershell
# Ejecutar test de mantenimiento forzando la condición
$env:FORCE_MAINTENANCE = "1"
pytest -v tests/test_transferencias.py::test_06_transferencia_en_mantenimiento

# Limpiar variable
Remove-Item Env:\FORCE_MAINTENANCE
```

#### Test 12: Cuenta Bloqueada

```powershell
# Ejecutar test de cuenta bloqueada
$env:BLOCKED_ACCOUNT = "99999999"
pytest -v tests/test_transferencias.py::test_12_cuenta_origen_bloqueada

# Limpiar variable
Remove-Item Env:\BLOCKED_ACCOUNT
```

### Ejecutar TODOS los Tests (15/15)

```powershell
# Configurar todas las variables para ejecutar los 15 tests
$env:AUTH_TOKEN = "Bearer test"
$env:FORCE_MAINTENANCE = "1"
$env:BLOCKED_ACCOUNT = "99999999"

# Ejecutar tests
pytest -v

# Resultado esperado: 15 passed in ~80s
```

### Configuración de Timeout

```powershell
# Ejecutar tests con timeout de 5 minutos
pytest -v --timeout=300
```

### Ejecutar Tests en Paralelo

```powershell
# Instalar plugin de paralelización
pip install pytest-xdist

# Ejecutar tests en paralelo (4 workers)
pytest -v -n 4
```

### Modo Debug

```powershell
# Ejecutar con modo debug de Python
python -m pdb -c continue -m pytest -v

# Ejecutar con logs detallados
pytest -v --log-cli-level=DEBUG
```

---

## ❌ Resolución de Problemas

### Problema 1: Puerto 8000 Ocupado

**Error:**
```
OSError: [WinError 10048] Only one usage of each socket address
```

**Solución:**
```powershell
# Ver qué proceso usa el puerto 8000
netstat -ano | findstr :8000

# Detener proceso Python
Get-Process python | Stop-Process -Force

# O cambiar puerto en main.py
# uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Problema 2: Tests Se Saltan

**Error:**
```
2 skipped: API endpoint no disponible
```

**Solución:**
```powershell
# Verificar que la API está corriendo
curl http://localhost:8000/health

# Si no responde, iniciar API
python main.py
```

### Problema 3: Token de Autenticación No Configurado

**Error:**
```
AssertionError: expected 200, got 401
```

**Solución:**
```powershell
# Configurar token antes de ejecutar tests
$env:AUTH_TOKEN = "Bearer test"
pytest -v
```

### Problema 4: Módulos No Encontrados

**Error:**
```
ModuleNotFoundError: No module named 'pytest'
```

**Solución:**
```powershell
# Reinstalar dependencias
python -m pip install -r requirements.txt

# Verificar instalación
pip list | Select-String "pytest"
```

### Problema 5: Tests Fallan por Límites Agotados

**Error:**
```
AssertionError: Expected 200, got 403 - Límite diario excedido
```

**Solución:**
```powershell
# Resetear límites de cuenta
curl -X POST http://localhost:8000/api/cuentas/12345678/reset

# O reiniciar API (limpia estado en memoria)
# Ctrl+C en terminal de API, luego:
python main.py
```

### Problema 6: Encoding en Windows

**Error:**
```
UnicodeEncodeError: 'charmap' codec can't encode character
```

**Solución:**
```powershell
# Configurar encoding UTF-8
$env:PYTHONIOENCODING = "utf-8"
pytest -v
```

### Problema 7: Permisos de Ejecución de Scripts

**Error:**
```
cannot be loaded because running scripts is disabled
```

**Solución:**
```powershell
# Cambiar política de ejecución (como Administrador)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# O ejecutar script con bypass
powershell -ExecutionPolicy Bypass -File .\run_tests_sve.ps1
```

---

## 📚 Comandos Útiles de Referencia Rápida

### Comandos Básicos

```powershell
# Instalar dependencias
pip install -r requirements.txt

# Iniciar API
python main.py

# Ejecutar tests
$env:AUTH_TOKEN="Bearer test"; pytest -v

# Ejecutar tests + reportes SVE
.\run_tests_sve.ps1

# Verificar salud de API
curl http://localhost:8000/health
```

### Comandos de Limpieza

```powershell
# Limpiar cache de pytest
Remove-Item -Recurse -Force .pytest_cache

# Limpiar reportes
Remove-Item report.html, sve_report.*, .coverage -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force htmlcov

# Limpiar archivos Python compilados
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item
Get-ChildItem -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force
```

### Comandos de Diagnóstico

```powershell
# Ver versiones de paquetes
pip list

# Ver información de pytest
pytest --version
pytest --fixtures

# Ver estructura de tests
pytest --collect-only

# Ver cobertura simple
pytest --cov=main --cov-report=term
```

---

## 🎯 Flujo de Trabajo Recomendado

### Para Desarrollo Diario

```powershell
# 1. Iniciar API (terminal 1)
python main.py

# 2. Ejecutar tests (terminal 2)
$env:AUTH_TOKEN="Bearer test"
pytest -v

# 3. Ver resultados
start report.html
```

### Para Entrega/Demostración

```powershell
# Ejecución completa con todos los reportes
.\run_tests_sve.ps1

# Verificar resultados
code sve_report.json
start report.html
start sve_report.csv
```

### Para CI/CD

```powershell
# Script de integración continua
python -m pip install -r requirements.txt
$env:AUTH_TOKEN="Bearer test"
pytest -v --junitxml=junit.xml --cov=main --cov-report=xml
```

---

## 📖 Documentación Adicional

Para más información, consulta estos archivos:

| Documento | Contenido |
|-----------|-----------|
| [README.md](./README.md) | Inicio rápido del proyecto |
| [DOCUMENTACION_TECNICA.md](./DOCUMENTACION_TECNICA.md) | Especificaciones técnicas completas |
| [DOCUMENTACION_SVE.md](./DOCUMENTACION_SVE.md) | Guía de reportes SVE |
| [COMANDOS_UTILES.md](./COMANDOS_UTILES.md) | Referencia completa de comandos |
| [RESUMEN_EJECUTIVO.md](./RESUMEN_EJECUTIVO.md) | Overview del proyecto |
| [INDICE.md](./INDICE.md) | Índice general del proyecto |

---

## 🎓 Próximos Pasos

Una vez completada la configuración:

1. ✅ **Ejecutar la automatización**: `.\run_tests_sve.ps1`
2. ✅ **Revisar reportes SVE**: Ver XML, JSON y CSV
3. ✅ **Analizar resultados**: Verificar Pass Rate ≥ 86%
4. ✅ **Explorar API**: Abrir http://localhost:8000/docs
5. ✅ **Importar Postman**: Usar `Transferencias_Bancarias.postman_collection.json`
6. ✅ **Modificar tests**: Agregar nuevos casos en `tests/test_transferencias.py`

---

## ✅ Checklist de Verificación

Antes de ejecutar la automatización, verifica:

- [ ] Python 3.8+ instalado (`python --version`)
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] En directorio correcto del proyecto
- [ ] Puerto 8000 disponible (no usado por otro proceso)
- [ ] Variable `AUTH_TOKEN` configurada
- [ ] API respondiendo en http://localhost:8000/health

Si todos los ítems están marcados, ejecuta:
```powershell
.\run_tests_sve.ps1
```

---

**Versión**: 1.0  
**Fecha**: 10 de diciembre de 2025  
**Autor**: QA Senior - Banca Digital  
**Proyecto**: API Transferencias Bancarias - Testing Automatizado
