# Manual de Pruebas - Bureau de Crédito

## Índice
1. [Introducción](#introducción)
2. [Configuración del Entorno](#configuración-del-entorno)
3. [Estructura de Pruebas](#estructura-de-pruebas)
4. [Casos de Prueba Detallados](#casos-de-prueba-detallados)
5. [Ejecución](#ejecución)
6. [Interpretación de Resultados](#interpretación-de-resultados)
7. [Troubleshooting](#troubleshooting)

## Introducción

Suite de pruebas automatizadas para validar el sistema de consulta de Bureau de Crédito, crítico para decisiones crediticias en sistemas bancarios.

### Objetivos
- ✅ Validar integración con Bureau de Crédito externo
- ✅ Verificar reglas de negocio crediticio
- ✅ Asegurar manejo correcto de errores
- ✅ Garantizar cumplimiento normativo
- ✅ Validar tiempos de respuesta

### Cobertura
- **15 casos de prueba** cubriendo:
  - Path feliz y casos positivos (4)
  - Validaciones de entrada (3)
  - Manejo de errores (3)
  - Edge cases (5)

## Configuración del Entorno

### Prerequisitos
```powershell
# Python 3.8 o superior
python --version

# Pip actualizado
python -m pip install --upgrade pip
```

### Instalación
```powershell
# 1. Clonar o navegar al repositorio
cd CapacitacionIA-Banistmo

# 2. Crear entorno virtual (recomendado)
python -m venv venv
.\venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con valores correctos
```

### Configuración de .env
```ini
# URL del API (ajustar según ambiente)
API_BASE_URL=http://localhost:8000

# Timeout en segundos
API_TIMEOUT=5

# Ambiente de pruebas
TEST_ENVIRONMENT=dev
```

## Estructura de Pruebas

```
tests/
├── conftest.py                      # Configuración global y fixtures
├── test_bureau_happy_path.py        # TC-BC-001 a TC-BC-004
├── test_bureau_validations.py      # TC-BC-005 a TC-BC-007
├── test_bureau_errors.py            # TC-BC-008, TC-BC-009, TC-BC-015
├── test_bureau_edge_cases.py       # TC-BC-010 a TC-BC-014
├── test_data/
│   └── bureau_test_data.py          # Datos de prueba centralizados
└── helpers/
    └── api_client.py                # Cliente HTTP helper
```

## Casos de Prueba Detallados

### Suite 1: Happy Path (P0 - Crítica)

#### TC-BC-001: Cliente con Buen Historial ⭐
```python
# Archivo: test_bureau_happy_path.py
# Marker: @pytest.mark.critical

Documento: 1234567890
Score esperado: >= 700
Estado: APROBADO
Tiempo: < 3s
```

#### TC-BC-002: Cliente con Deudas Activas ⭐
```python
Documento: 2345678901
Score esperado: 650-699
Estado: REVISAR
```

#### TC-BC-003: Cliente Moroso ⭐
```python
Documento: 3456789012
Score esperado: < 500
Estado: RECHAZADO
Días mora: > 0
```

#### TC-BC-004: Cliente en CIFIN ⭐
```python
Documento: 4567890123
Estado: RECHAZADO
en_cifin: true
```

### Suite 2: Validaciones (P1 - Alta)

#### TC-BC-005: Documento Inválido
```python
Documento: "123-456*789"
Status esperado: 422
Error: Validación de formato
```

#### TC-BC-006: Longitud Incorrecta
```python
Documento: "12345" (< 6 dígitos)
Status esperado: 422
```

#### TC-BC-007: Tipo Documento Inválido
```python
tipo_documento: "XXX"
Status esperado: 422
Válidos: CC, CE, NIT, PAS
```

### Suite 3: Manejo de Errores (P0-P1)

#### TC-BC-008: Timeout ⭐
```python
Timeout configurado: 5 segundos
Status esperado: 503/504 o Timeout Exception
```

#### TC-BC-009: Respuesta Inválida
```python
Status esperado: 502 Bad Gateway
Manejo de JSON malformado
```

#### TC-BC-015: Campo Null
```python
documento: null
Status esperado: 422
Error: Campo requerido
```

### Suite 4: Edge Cases (P1-P2)

#### TC-BC-010: Cliente Extranjero
```python
Documento: "AB123456"
tipo_documento: "PAS"
Score: null
sin_historial_local: true
```

#### TC-BC-011: Sin Historial
```python
Documento: 6789012345
Score: null
Estado: REQUIERE_ANALISIS_MANUAL
```

#### TC-BC-012: Consulta Simultánea
```python
Mismo documento, 2 requests simultáneos
Ambos deben retornar 200
Misma información
```

#### TC-BC-013: Consulta Histórica
```python
GET /api/bureau/{cliente_id}
Verificar cache y timestamp
```

#### TC-BC-014: Score Límite
```python
Score: 600 (frontera)
Estado: REVISAR
requiere_aprobacion_gerencia: true
```

## Ejecución

### Comandos Básicos

```powershell
# Todas las pruebas
pytest

# Con reporte detallado
pytest -v

# Solo críticas (P0) - para deployment
pytest -m critical

# Críticas + Alta prioridad (P0 + P1) - para releases
pytest -m "critical or high"

# Suite completa con todas las prioridades
pytest -m "critical or high or medium"
```

### Por Tipo de Prueba

```powershell
# Suite de regresión
pytest -m regression

# Pruebas de validación
pytest -m validation

# Edge cases
pytest -m edge_case

# Smoke tests
pytest -m smoke
```

### Por Archivo

```powershell
# Path feliz
pytest tests/test_bureau_happy_path.py

# Validaciones
pytest tests/test_bureau_validations.py

# Errores
pytest tests/test_bureau_errors.py

# Edge cases
pytest tests/test_bureau_edge_cases.py
```

### Test Específico

```powershell
pytest tests/test_bureau_happy_path.py::TestBureauHappyPath::test_tc_bc_001_cliente_buen_historial -v
```

### Con Reportes

```powershell
# Reporte HTML
pytest --html=report.html --self-contained-html

# Reporte JUnit (para CI/CD)
pytest --junitxml=report.xml

# Con cobertura
pytest --cov=tests --cov-report=html
```

### Usando el Script Python

```powershell
# Todas las pruebas
python run_tests.py all

# Solo críticas
python run_tests.py critical

# Críticas + Alta
python run_tests.py high

# Smoke tests
python run_tests.py smoke

# Suite de regresión
python run_tests.py regression
```

## Interpretación de Resultados

### Output Exitoso
```
tests/test_bureau_happy_path.py::TestBureauHappyPath::test_tc_bc_001_cliente_buen_historial PASSED [25%]
tests/test_bureau_happy_path.py::TestBureauHappyPath::test_tc_bc_002_cliente_deudas_activas_al_dia PASSED [50%]
...

============================== 15 passed in 5.23s ===============================
```

### Output con Fallos
```
tests/test_bureau_happy_path.py::TestBureauHappyPath::test_tc_bc_001_cliente_buen_historial FAILED [25%]

__________________________________ FAILURES _____________________________________
______________ TestBureauHappyPath.test_tc_bc_001_cliente_buen_historial _______________

    def test_tc_bc_001_cliente_buen_historial(self, api_client, verificar_api_disponible):
>       assert response.status_code == 200
E       AssertionError: Status code incorrecto: 500

tests/test_bureau_happy_path.py:42: AssertionError
```

### Markers y Símbolos
- ✓ `PASSED` - Test exitoso
- ✗ `FAILED` - Test falló
- `s` `SKIPPED` - Test omitido (API no disponible)
- `x` `XFAIL` - Fallo esperado
- `X` `XPASS` - Pasó cuando se esperaba fallo

## Troubleshooting

### API no está disponible
```
SKIPPED [1] tests/conftest.py:45: API no responde
```
**Solución**: Verificar que el API esté corriendo en localhost:8000

```powershell
# Verificar si el servicio está corriendo
Test-NetConnection -ComputerName localhost -Port 8000
```

### Timeout en las pruebas
```
requests.exceptions.Timeout: ...
```
**Solución**: Ajustar timeout en .env o verificar conectividad

```ini
# Aumentar timeout a 10 segundos
API_TIMEOUT=10
```

### Errores de importación
```
ModuleNotFoundError: No module named 'pytest'
```
**Solución**: Instalar dependencias

```powershell
pip install -r requirements.txt
```

### Tests fallan por datos incorrectos
**Solución**: Verificar que el API tenga los datos de prueba esperados o ajustar `test_data/bureau_test_data.py`

### Variables de entorno no cargadas
```
KeyError: 'API_BASE_URL'
```
**Solución**: Crear archivo .env desde .env.example

```powershell
cp .env.example .env
```

## Mejores Prácticas

### Antes de Cada Ejecución
1. ✅ Verificar que el API esté corriendo
2. ✅ Revisar archivo .env
3. ✅ Activar entorno virtual
4. ✅ Actualizar dependencias si es necesario

### En CI/CD
```yaml
# Ejemplo para GitHub Actions
- name: Run Critical Tests
  run: pytest -m critical --junitxml=report.xml
  
- name: Run Full Regression
  run: pytest -m regression --html=report.html
```

### Reportar Issues
Al reportar un test fallido, incluir:
- Comando ejecutado
- Output completo del test
- Versión de Python y dependencias
- Configuración de .env (sin datos sensibles)
- Logs del API si están disponibles

## Mantenimiento

### Actualizar Datos de Prueba
Editar `tests/test_data/bureau_test_data.py`

### Agregar Nuevos Tests
1. Identificar suite apropiada
2. Agregar marcadores correctos
3. Seguir convención de nombres: `test_tc_bc_XXX_descripcion`
4. Documentar con docstring completo
5. Agregar datos en bureau_test_data.py

### Ejecutar Tests Localmente Antes de Commit
```powershell
# Validación mínima
pytest -m "critical or high" -v
```

## Contacto y Soporte

Para preguntas o issues:
- Revisar documentación del API: http://localhost:8000/docs
- Consultar este manual
- Contactar al equipo de QA
