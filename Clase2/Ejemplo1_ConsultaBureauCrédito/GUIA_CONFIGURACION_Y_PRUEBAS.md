# 🧪 Guía Completa de Configuración y Ejecución de Tests - Bureau de Crédito

## 📋 Tabla de Contenidos
1. [Requisitos Previos](#requisitos-previos)
2. [Instalación Paso a Paso](#instalación-paso-a-paso)
3. [Configuración del Entorno](#configuración-del-entorno)
4. [Verificación de la Instalación](#verificación-de-la-instalación)
5. [Ejecución de Tests](#ejecución-de-tests)
6. [Interpretación de Resultados](#interpretación-de-resultados)
7. [Troubleshooting](#troubleshooting)
8. [Ejemplos Prácticos](#ejemplos-prácticos)

---

## 📌 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

### Software Requerido
- ✅ **Python 3.8 o superior**
- ✅ **pip** (gestor de paquetes de Python)
- ✅ **PowerShell** (Windows)
- ✅ **Git** (opcional, para control de versiones)

### API del Bureau de Crédito
- ✅ API corriendo en `localhost:8000`
- ✅ Acceso a la documentación en `http://localhost:8000/docs`

### Verificar Instalaciones

```powershell
# Verificar Python
python --version
# Debe mostrar: Python 3.8.x o superior

# Verificar pip
pip --version
# Debe mostrar: pip 20.x.x o superior

# Verificar conectividad del API
Test-NetConnection -ComputerName localhost -Port 8000
```

---

## 🚀 Instalación Paso a Paso

### Paso 1: Navegar al Directorio del Proyecto

```powershell
cd C:\Users\1577089\Desktop\CapacitacionIA-Banistmo\CapacitacionIA-Banistmo
```

### Paso 2: Crear Entorno Virtual (Recomendado)

Un entorno virtual mantiene las dependencias aisladas del sistema.

```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\activate

# Verás (venv) al inicio de tu línea de comando
# (venv) PS C:\Users\1577089\Desktop\...>
```

**Nota:** Para desactivar el entorno virtual más tarde, usa:
```powershell
deactivate
```

### Paso 3: Instalar Dependencias

```powershell
# Con el entorno virtual activado, instalar todas las dependencias
pip install -r requirements.txt

# Esto instalará:
# - pytest 7.4.3
# - pytest-asyncio 0.21.1
# - pytest-timeout 2.2.0
# - pytest-mock 3.12.0
# - requests 2.31.0
# - httpx 0.25.2
# - faker 20.1.0
# - pydantic 2.5.2
# - python-dotenv 1.0.0
```

### Paso 4: Verificar Instalación de pytest

```powershell
pytest --version

# Salida esperada:
# pytest 7.4.3
```

---

## ⚙️ Configuración del Entorno

### Paso 1: Configurar Variables de Entorno

El archivo `.env` ya está creado con valores por defecto. Si necesitas modificarlo:

```powershell
# Ver contenido del archivo .env
cat .env
```

**Contenido del archivo `.env`:**
```ini
# Configuración del API
API_BASE_URL=http://localhost:8000
API_TIMEOUT=5

# Configuración de pruebas
TEST_ENVIRONMENT=dev
ENABLE_MOCK=false
```

### Paso 2: Ajustar Configuración (Opcional)

Si tu API está en una URL diferente o necesitas cambiar el timeout:

```powershell
# Editar archivo .env con notepad
notepad .env

# O con VS Code
code .env
```

**Configuraciones comunes:**

| Variable | Descripción | Valores Posibles |
|----------|-------------|------------------|
| `API_BASE_URL` | URL del API Bureau | `http://localhost:8000` (local)<br>`https://api-dev.banco.com` (dev)<br>`https://api.banco.com` (prod) |
| `API_TIMEOUT` | Timeout en segundos | `5` (default)<br>`10` (para conexiones lentas) |
| `TEST_ENVIRONMENT` | Ambiente de pruebas | `dev`, `qa`, `uat`, `prod` |
| `ENABLE_MOCK` | Usar datos mock | `true`, `false` |

---

## ✅ Verificación de la Instalación

### Checklist de Verificación

Ejecuta estos comandos para confirmar que todo está configurado correctamente:

#### 1. Verificar Python y pip
```powershell
python --version  # Debe mostrar 3.8+
pip --version     # Debe estar instalado
```

#### 2. Verificar entorno virtual activo
```powershell
# Debes ver (venv) en tu prompt
# (venv) PS C:\Users\...>
```

#### 3. Verificar pytest instalado
```powershell
pytest --version

# Salida esperada:
# pytest 7.4.3
```

#### 4. Listar tests disponibles
```powershell
pytest --collect-only

# Salida esperada: Lista de 21 tests
```

#### 5. Verificar estructura de archivos
```powershell
# Listar archivos de tests
ls tests\*.py

# Debes ver:
# test_bureau_happy_path.py
# test_bureau_validations.py
# test_bureau_errors.py
# test_bureau_edge_cases.py
# conftest.py
```

#### 6. Verificar API disponible
```powershell
# Opción 1: PowerShell
Test-NetConnection -ComputerName localhost -Port 8000

# Opción 2: Navegador
# Abrir: http://localhost:8000/docs
```

### Script de Verificación Completo

```powershell
# Ejecutar todas las verificaciones en secuencia
Write-Host "=== VERIFICACIÓN DE INSTALACIÓN ===" -ForegroundColor Cyan

Write-Host "`n1. Verificando Python..." -ForegroundColor Yellow
python --version

Write-Host "`n2. Verificando pytest..." -ForegroundColor Yellow
pytest --version

Write-Host "`n3. Verificando archivo .env..." -ForegroundColor Yellow
if (Test-Path .env) { Write-Host "✓ Archivo .env encontrado" -ForegroundColor Green } else { Write-Host "✗ Archivo .env no encontrado" -ForegroundColor Red }

Write-Host "`n4. Verificando estructura de tests..." -ForegroundColor Yellow
$testFiles = @("tests\test_bureau_happy_path.py", "tests\test_bureau_validations.py", "tests\test_bureau_errors.py", "tests\test_bureau_edge_cases.py")
foreach ($file in $testFiles) {
    if (Test-Path $file) { Write-Host "✓ $file" -ForegroundColor Green } else { Write-Host "✗ $file" -ForegroundColor Red }
}

Write-Host "`n5. Contando tests disponibles..." -ForegroundColor Yellow
pytest --collect-only -q

Write-Host "`n6. Verificando conectividad del API..." -ForegroundColor Yellow
Test-NetConnection -ComputerName localhost -Port 8000

Write-Host "`n=== VERIFICACIÓN COMPLETADA ===" -ForegroundColor Cyan
```

---

## 🎯 Ejecución de Tests

### Comandos Básicos

#### Ejecutar TODOS los tests
```powershell
pytest

# Salida esperada: 21 tests ejecutados
# ========================= 21 passed in 5.23s =========================
```

#### Ejecutar con salida detallada (verbose)
```powershell
pytest -v

# Muestra cada test con su nombre completo y resultado
```

#### Ejecutar con salida muy detallada
```powershell
pytest -vv

# Incluye información adicional de debugging
```

### Ejecución por Prioridad

#### Solo tests CRÍTICOS (P0) - 5 tests
```powershell
pytest -m critical

# Ejecuta solo los casos bloqueantes:
# - TC-BC-001: Cliente con buen historial
# - TC-BC-002: Cliente con deudas activas
# - TC-BC-003: Cliente moroso
# - TC-BC-004: Cliente en CIFIN
# - TC-BC-008: Timeout
```

#### Tests Críticos + Alta Prioridad (P0 + P1) - 15 tests
```powershell
pytest -m "critical or high"

# Ejecuta todos los casos importantes para releases
```

#### Todos los tests por prioridad
```powershell
pytest -m "critical or high or medium"

# Ejecuta los 21 tests completos
```

### Ejecución por Tipo de Test

#### Suite de Regresión
```powershell
pytest -m regression

# Ejecuta 13 tests de regresión
```

#### Tests de Validación
```powershell
pytest -m validation

# Ejecuta 9 tests de validación de entrada
```

#### Tests de Integración
```powershell
pytest -m integration

# Ejecuta 10 tests de integración con el API
```

#### Edge Cases
```powershell
pytest -m edge_case

# Ejecuta 6 tests de casos extremos
```

#### Smoke Tests
```powershell
pytest -m smoke

# Ejecuta 4 tests básicos de humo
```

### Ejecución por Archivo

#### Path Feliz y Casos Positivos
```powershell
pytest tests/test_bureau_happy_path.py

# Ejecuta 4 tests (TC-BC-001 a TC-BC-004)
```

#### Validaciones de Entrada
```powershell
pytest tests/test_bureau_validations.py

# Ejecuta 6 tests (TC-BC-005 a TC-BC-007 + extras)
```

#### Manejo de Errores
```powershell
pytest tests/test_bureau_errors.py

# Ejecuta 5 tests (TC-BC-008, TC-BC-009, TC-BC-015 + extras)
```

#### Edge Cases y Casos Especiales
```powershell
pytest tests/test_bureau_edge_cases.py

# Ejecuta 6 tests (TC-BC-010 a TC-BC-014 + extras)
```

### Ejecución de Tests Específicos

#### Por clase de test
```powershell
pytest tests/test_bureau_happy_path.py::TestBureauHappyPath

# Ejecuta todos los tests de la clase TestBureauHappyPath
```

#### Por test individual
```powershell
pytest tests/test_bureau_happy_path.py::TestBureauHappyPath::test_tc_bc_001_cliente_buen_historial

# Ejecuta solo el test TC-BC-001
```

#### Múltiples tests específicos
```powershell
pytest tests/test_bureau_happy_path.py::TestBureauHappyPath::test_tc_bc_001_cliente_buen_historial tests/test_bureau_happy_path.py::TestBureauHappyPath::test_tc_bc_004_cliente_en_lista_cifin

# Ejecuta TC-BC-001 y TC-BC-004
```

### Opciones Útiles de Ejecución

#### Detener en el primer error
```powershell
pytest -x

# Se detiene apenas encuentra un test fallido
```

#### Mostrar prints y logs
```powershell
pytest -s

# Muestra todos los print() y logs durante la ejecución
```

#### Modo quiet (silencioso)
```powershell
pytest -q

# Muestra solo resumen final
```

#### Ejecutar últimos tests fallidos
```powershell
pytest --lf

# Solo ejecuta los tests que fallaron en la última ejecución
```

#### Ejecutar primero los fallidos, luego todos
```powershell
pytest --ff

# Ejecuta primero los fallidos, después el resto
```

### Generación de Reportes

#### Reporte HTML
```powershell
# Instalar plugin (si no está instalado)
pip install pytest-html

# Generar reporte
pytest --html=report.html --self-contained-html

# Abrir reporte
start report.html
```

#### Reporte JUnit XML (para CI/CD)
```powershell
pytest --junitxml=report.xml

# Archivo XML compatible con Jenkins, GitLab CI, etc.
```

#### Reporte con Cobertura
```powershell
# Instalar plugin de cobertura
pip install pytest-cov

# Generar reporte de cobertura
pytest --cov=tests --cov-report=html

# Abrir reporte
start htmlcov/index.html
```

### Usando el Script Python

```powershell
# Todas las pruebas
python run_tests.py all

# Solo críticas (P0)
python run_tests.py critical

# Críticas + Alta (P0 + P1)
python run_tests.py high

# Smoke tests
python run_tests.py smoke

# Suite de regresión
python run_tests.py regression
```

---

## 📊 Interpretación de Resultados

### Símbolos y Estados

| Símbolo | Estado | Significado |
|---------|--------|-------------|
| `.` | PASSED | Test pasó exitosamente ✅ |
| `F` | FAILED | Test falló ❌ |
| `s` | SKIPPED | Test fue omitido ⏭️ |
| `x` | XFAIL | Fallo esperado (xfail) ⚠️ |
| `X` | XPASS | Pasó cuando se esperaba fallo 🎉 |
| `E` | ERROR | Error durante ejecución 💥 |

### Ejemplo de Salida Exitosa

```
tests/test_bureau_happy_path.py ....                                    [ 19%]
tests/test_bureau_validations.py ......                                 [ 47%]
tests/test_bureau_errors.py .....                                       [ 71%]
tests/test_bureau_edge_cases.py ......                                  [100%]

========================= 21 passed in 5.23s ==========================
```

**Interpretación:**
- ✅ Todos los tests pasaron (21/21)
- ⏱️ Tiempo total: 5.23 segundos
- 📊 Distribución por archivo visible

### Ejemplo de Salida con Fallos

```
tests/test_bureau_happy_path.py .F..                                    [ 19%]

=================================== FAILURES ===================================
____________ TestBureauHappyPath.test_tc_bc_002_cliente_deudas_activas_al_dia ___________

self = <tests.test_bureau_happy_path.TestBureauHappyPath object at 0x...>
api_client = <tests.helpers.api_client.BureauAPIClient object at 0x...>

    def test_tc_bc_002_cliente_deudas_activas_al_dia(self, api_client, verificar_api_disponible):
        response = api_client.consultar_bureau(
            documento=CLIENTE_DEUDAS_ACTIVAS["documento"],
            tipo_documento=CLIENTE_DEUDAS_ACTIVAS["tipo_documento"]
        )
        
>       assert response.status_code == 200
E       AssertionError: assert 500 == 200
E        +  where 500 = <Response [500]>.status_code

tests/test_bureau_happy_path.py:85: AssertionError
======================= short test summary info ========================
FAILED tests/test_bureau_happy_path.py::TestBureauHappyPath::test_tc_bc_002_cliente_deudas_activas_al_dia
==================== 1 failed, 20 passed in 5.45s =====================
```

**Interpretación:**
- ❌ 1 test falló: `test_tc_bc_002_cliente_deudas_activas_al_dia`
- ✅ 20 tests pasaron
- 🔍 Error: El API retornó status 500 en lugar de 200
- 📍 Línea del error: `tests/test_bureau_happy_path.py:85`

### Ejemplo de Tests Omitidos (Skipped)

```
tests/test_bureau_happy_path.py ssss                                    [ 19%]

========================= 4 skipped in 0.52s ===========================
```

**Razones comunes para skip:**
- 🔌 API no está disponible
- ⚙️ Configuración incorrecta
- 🏷️ Test marcado para skip con `@pytest.mark.skip`

### Resumen de Estadísticas

Al final de cada ejecución verás un resumen:

```
========================= test session starts ==========================
platform win32 -- Python 3.11.0, pytest-7.4.3, pluggy-1.3.0
rootdir: C:\Users\1577089\Desktop\CapacitacionIA-Banistmo\CapacitacionIA-Banistmo
configfile: pytest.ini
testpaths: tests
plugins: asyncio-0.21.1, timeout-2.2.0, mock-3.12.0
collected 21 items

tests/test_bureau_happy_path.py ....                                    [ 19%]
tests/test_bureau_validations.py ......                                 [ 47%]
tests/test_bureau_errors.py .....                                       [ 71%]
tests/test_bureau_edge_cases.py ......                                  [100%]

========================= 21 passed in 5.23s ===========================
```

---

## 🔧 Troubleshooting

### Problema 1: pytest no se reconoce

**Error:**
```
pytest : El término 'pytest' no se reconoce como nombre de un cmdlet...
```

**Solución:**
```powershell
# 1. Activar entorno virtual
.\venv\Scripts\activate

# 2. Verificar que pytest esté instalado
pip list | Select-String "pytest"

# 3. Si no está, instalarlo
pip install -r requirements.txt

# 4. Verificar instalación
pytest --version
```

### Problema 2: API no está disponible

**Error:**
```
SKIPPED [1] tests/conftest.py:45: API no responde
```

**Solución:**
```powershell
# 1. Verificar que el API esté corriendo
Test-NetConnection -ComputerName localhost -Port 8000

# 2. Verificar en navegador
start http://localhost:8000/docs

# 3. Si el API está en otra URL, actualizar .env
notepad .env
# Cambiar API_BASE_URL según corresponda

# 4. Reiniciar el API si es necesario
```

### Problema 3: Timeout en tests

**Error:**
```
requests.exceptions.Timeout: HTTPConnectionPool(host='localhost', port=8000): Read timed out.
```

**Solución:**
```powershell
# 1. Aumentar timeout en .env
notepad .env
# Cambiar API_TIMEOUT=5 a API_TIMEOUT=10

# 2. O ejecutar con marker excluyendo timeout
pytest -m "not timeout"

# 3. Verificar que el API responda rápido
# curl o Postman para probar manualmente
```

### Problema 4: ModuleNotFoundError

**Error:**
```
ModuleNotFoundError: No module named 'pytest'
ModuleNotFoundError: No module named 'requests'
```

**Solución:**
```powershell
# 1. Activar entorno virtual
.\venv\Scripts\activate

# 2. Reinstalar dependencias
pip install -r requirements.txt

# 3. Verificar instalación
pip list
```

### Problema 5: Tests fallan por datos incorrectos

**Error:**
```
AssertionError: Status code esperado 200, recibido: 404
```

**Solución:**
```powershell
# 1. Verificar que el API tenga los datos de prueba esperados
# Revisar: tests/test_data/bureau_test_data.py

# 2. Ajustar datos de prueba según tu API
notepad tests\test_data\bureau_test_data.py

# 3. O configurar API mock
# En .env: ENABLE_MOCK=true
```

### Problema 6: Variables de entorno no cargadas

**Error:**
```
KeyError: 'API_BASE_URL'
```

**Solución:**
```powershell
# 1. Verificar que existe .env
if (Test-Path .env) { "Archivo existe" } else { "Archivo NO existe" }

# 2. Si no existe, crearlo desde el ejemplo
cp .env.example .env

# 3. Verificar contenido
cat .env

# 4. Editar si es necesario
notepad .env
```

### Problema 7: Permisos de ejecución en Windows

**Error:**
```
cannot be loaded because running scripts is disabled on this system
```

**Solución:**
```powershell
# Ejecutar PowerShell como Administrador y ejecutar:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Luego reintenta activar el entorno virtual
.\venv\Scripts\activate
```

### Problema 8: Puerto 8000 ocupado

**Error:**
```
Connection refused [Errno 111]
```

**Solución:**
```powershell
# 1. Verificar qué proceso usa el puerto 8000
netstat -ano | findstr :8000

# 2. Detener el proceso si es necesario
# Anota el PID y ejecuta:
Stop-Process -Id <PID>

# 3. O cambiar la URL en .env a otro puerto
notepad .env
# API_BASE_URL=http://localhost:8001
```

---

## 💡 Ejemplos Prácticos

### Ejemplo 1: Primera Ejecución Completa

```powershell
# Paso 1: Ir al directorio
cd C:\Users\1577089\Desktop\CapacitacionIA-Banistmo\CapacitacionIA-Banistmo

# Paso 2: Activar entorno virtual
.\venv\Scripts\activate

# Paso 3: Verificar API
start http://localhost:8000/docs

# Paso 4: Ejecutar solo tests críticos primero
pytest -m critical -v

# Paso 5: Si todo pasa, ejecutar suite completa
pytest -v

# Paso 6: Generar reporte HTML
pytest --html=report.html --self-contained-html
start report.html
```

### Ejemplo 2: Debugging de un Test Específico

```powershell
# Ejecutar un test específico con máximo detalle
pytest tests/test_bureau_happy_path.py::TestBureauHappyPath::test_tc_bc_001_cliente_buen_historial -vv -s

# Explicación de flags:
# -vv: Muy verbose (máximo detalle)
# -s: Muestra prints y outputs
```

### Ejemplo 3: Ejecutar Solo Tests Rápidos

```powershell
# Ejecutar solo tests de validación (sin integración real)
pytest -m validation -v

# Son más rápidos porque no dependen tanto del API
```

### Ejemplo 4: Pipeline de CI/CD

```powershell
# Simular ejecución de CI/CD

# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar tests críticos con reporte JUnit
pytest -m critical --junitxml=report.xml -v

# 3. Si críticos pasan, ejecutar suite completa
if ($LASTEXITCODE -eq 0) {
    pytest --junitxml=full_report.xml -v
}

# 4. Generar reporte HTML
pytest --html=report.html --self-contained-html
```

### Ejemplo 5: Desarrollo Diario

```powershell
# Workflow típico durante desarrollo:

# 1. Activar entorno
.\venv\Scripts\activate

# 2. Hacer cambios en el código...

# 3. Ejecutar tests afectados
pytest tests/test_bureau_validations.py -v

# 4. Si pasa, ejecutar suite de regresión
pytest -m regression -x

# 5. Antes de commit, ejecutar críticos + alta
pytest -m "critical or high" -v
```

### Ejemplo 6: Análisis de Cobertura

```powershell
# Instalar plugin de cobertura
pip install pytest-cov

# Ejecutar con análisis de cobertura
pytest --cov=tests --cov-report=html --cov-report=term

# Ver reporte en terminal y HTML
start htmlcov/index.html
```

### Ejemplo 7: Ejecutar Tests en Paralelo (Más Rápido)

```powershell
# Instalar plugin de paralelización
pip install pytest-xdist

# Ejecutar tests en paralelo (4 workers)
pytest -n 4

# O usar todos los cores disponibles
pytest -n auto
```

---

## 📚 Referencias Adicionales

### Archivos de Documentación

- **QUICKSTART.md** - Guía rápida de 3 minutos
- **MANUAL_PRUEBAS.md** - Manual detallado con todos los casos
- **README.md** - Documentación principal del proyecto
- **VERIFICACION.md** - Checklist de verificación
- **RESUMEN.py** - Resumen ejecutable del proyecto

### Estructura de Tests

```
tests/
├── conftest.py                      # Fixtures y configuración global
├── test_bureau_happy_path.py        # 4 tests - Path feliz (TC-BC-001 a 004)
├── test_bureau_validations.py      # 6 tests - Validaciones (TC-BC-005 a 007)
├── test_bureau_errors.py            # 5 tests - Manejo errores (TC-BC-008, 009, 015)
├── test_bureau_edge_cases.py       # 6 tests - Edge cases (TC-BC-010 a 014)
├── helpers/
│   └── api_client.py                # Cliente HTTP reutilizable
└── test_data/
    └── bureau_test_data.py          # Datos centralizados
```

### Markers Disponibles

```python
@pytest.mark.critical     # Tests bloqueantes (P0)
@pytest.mark.high         # Alta prioridad (P1)
@pytest.mark.medium       # Prioridad media (P2)
@pytest.mark.smoke        # Tests de humo
@pytest.mark.regression   # Suite de regresión
@pytest.mark.integration  # Tests de integración
@pytest.mark.validation   # Validaciones de entrada
@pytest.mark.edge_case    # Casos extremos
@pytest.mark.timeout      # Tests con timeout
```

### Comandos Rápidos de Referencia

```powershell
# Activar entorno
.\venv\Scripts\activate

# Listar tests
pytest --collect-only

# Tests críticos
pytest -m critical

# Con reporte
pytest --html=report.html --self-contained-html

# Verbose
pytest -v

# Detener en error
pytest -x

# Solo último fallido
pytest --lf
```

---

## 🎓 Mejores Prácticas

### Antes de Ejecutar Tests

1. ✅ Activar entorno virtual
2. ✅ Verificar que el API esté corriendo
3. ✅ Revisar archivo .env
4. ✅ Ejecutar tests críticos primero

### Durante el Desarrollo

1. ✅ Ejecutar tests relacionados después de cada cambio
2. ✅ Usar `-x` para detener en primer error
3. ✅ Usar `-v` para ver detalles
4. ✅ Revisar logs con `-s` si hay fallos

### Antes de Commit

1. ✅ Ejecutar suite de regresión
2. ✅ Verificar que no hay tests skipped inesperadamente
3. ✅ Generar reporte si es necesario
4. ✅ Revisar cobertura de código

### En CI/CD

1. ✅ Ejecutar tests críticos primero
2. ✅ Generar reportes JUnit XML
3. ✅ Configurar timeout apropiado
4. ✅ Archivar reportes HTML

---

## 📞 Soporte

Para más ayuda:
- 📖 Consultar `MANUAL_PRUEBAS.md`
- 🚀 Ver `QUICKSTART.md`
- 🌐 Documentación API: http://localhost:8000/docs
- 📋 Casos de prueba SVE: `test_cases_sve.csv`, `test_cases_sve.txt`, `test_cases_sve.json`

---

## ✅ Checklist Final

Antes de comenzar, verifica:

- [ ] Python 3.8+ instalado
- [ ] pip actualizado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Archivo `.env` configurado
- [ ] API corriendo en localhost:8000
- [ ] pytest funcionando (`pytest --version`)
- [ ] Tests listados correctamente (`pytest --collect-only`)

**¡Listo para probar!** 🎉

```powershell
pytest -m critical -v
```

---

**Última actualización:** 2025-12-09  
**Versión:** 1.0  
**Proyecto:** Capacitación IA - Banistmo
