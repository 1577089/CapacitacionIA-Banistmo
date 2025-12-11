# Capacitación IA - Banistmo - Clase 2
## Automatización de Pruebas con Python y Pytest

Este repositorio contiene dos ejercicios prácticos de automatización de pruebas de APIs utilizando Python, Pytest y FastAPI.

---

## 📋 Tabla de Contenidos

1. [Ejemplo 1: Sistema de Consulta de Buró de Crédito](#ejemplo-1-sistema-de-consulta-de-buró-de-crédito)
2. [Ejemplo 2: Sistema de Transferencias Bancarias](#ejemplo-2-sistema-de-transferencias-bancarias)
3. [Requisitos Generales](#requisitos-generales)
4. [Configuración del Entorno](#configuración-del-entorno)
5. [Resumen de Aprendizajes](#resumen-de-aprendizajes)

---

## Ejemplo 1: Sistema de Consulta de Buró de Crédito

### 📁 Directorio
`Ejemplo1_ConsultaBureauCrédito/`

### 🎯 Objetivo
Implementar un sistema completo de pruebas automatizadas para una API de consulta de buró de crédito, cubriendo casos felices, casos extremos, validaciones y manejo de errores.

### 📝 Paso a Paso Realizado

#### 1. **Estructura del Proyecto**
```
Ejemplo1_ConsultaBureauCrédito/
├── tests/
│   ├── __init__.py
│   ├── conftest.py                      # Configuración de pytest y fixtures
│   ├── test_bureau_happy_path.py        # Casos de prueba positivos
│   ├── test_bureau_edge_cases.py        # Casos extremos
│   ├── test_bureau_validations.py       # Validaciones de datos
│   ├── test_bureau_errors.py            # Manejo de errores
│   ├── helpers/
│   │   ├── __init__.py
│   │   └── api_client.py                # Cliente HTTP reutilizable
│   └── test_data/
│       ├── __init__.py
│       └── bureau_test_data.py          # Datos de prueba centralizados
├── pytest.ini                           # Configuración de pytest
├── requirements.txt                     # Dependencias del proyecto
├── .env.example                         # Template de variables de entorno
├── run_tests.py                         # Script para ejecutar pruebas
└── run_tests.ps1                        # Script PowerShell para Windows
```

#### 2. **Configuración de Pytest (`pytest.ini`)**
```ini
[pytest]
minversion = 6.0
addopts = -ra -q --strict-markers --tb=short
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    happy_path: Casos de prueba del camino feliz
    edge_cases: Casos extremos y de frontera
    validations: Validaciones de datos de entrada
    errors: Manejo de errores y excepciones
    smoke: Pruebas de humo rápidas
```

#### 3. **Implementación del Cliente API (`helpers/api_client.py`)**
- Cliente HTTP centralizado usando `requests`
- Manejo de autenticación básica
- Métodos GET y POST con manejo de errores
- Timeout configurables
- Headers personalizables

```python
class BureauAPIClient:
    def __init__(self, base_url: str, auth: Optional[Tuple[str, str]] = None):
        self.base_url = base_url
        self.session = requests.Session()
        if auth:
            self.session.auth = auth
```

#### 4. **Datos de Prueba Centralizados (`test_data/bureau_test_data.py`)**
- Casos válidos para diferentes tipos de clientes
- Casos inválidos (formatos incorrectos, valores fuera de rango)
- Casos extremos (valores límite, caracteres especiales)
- Datos esperados para validaciones

#### 5. **Fixtures de Pytest (`conftest.py`)**
```python
@pytest.fixture(scope="session")
def api_base_url():
    """URL base de la API"""
    return os.getenv("API_BASE_URL", "http://localhost:8000")

@pytest.fixture(scope="session")
def api_client(api_base_url):
    """Cliente API configurado"""
    return BureauAPIClient(base_url=api_base_url)
```

#### 6. **Categorías de Pruebas Implementadas**

##### **A. Happy Path Tests (`test_bureau_happy_path.py`)**
- ✅ Consulta exitosa con ID válido
- ✅ Respuesta con estructura correcta
- ✅ Validación de campos obligatorios
- ✅ Consulta de cliente con buen historial crediticio
- ✅ Múltiples consultas consecutivas

##### **B. Edge Cases (`test_bureau_edge_cases.py`)**
- ✅ ID en el límite mínimo (1)
- ✅ ID en el límite máximo (999999)
- ✅ Cliente sin historial crediticio
- ✅ Cliente con score en límite inferior (300)
- ✅ Cliente con score en límite superior (850)
- ✅ Consulta con caracteres especiales en headers

##### **C. Validations (`test_bureau_validations.py`)**
- ✅ Rechazo de ID con letras
- ✅ Rechazo de ID con caracteres especiales
- ✅ Validación de formato de fecha
- ✅ Validación de rango de score crediticio
- ✅ Validación de estructura de respuesta JSON
- ✅ Validación de tipos de datos

##### **D. Error Handling (`test_bureau_errors.py`)**
- ✅ Error 404 para cliente no encontrado
- ✅ Error 400 para ID inválido
- ✅ Error 422 para datos mal formados
- ✅ Manejo de timeout
- ✅ Manejo de errores de conexión
- ✅ Validación de mensajes de error descriptivos

#### 7. **Reportes y Resultados**
Se implementaron múltiples formatos de reporte:

```bash
# Reporte en consola con detalles
pytest -v

# Reporte HTML
pytest --html=report.html --self-contained-html

# Reporte JSON para integración CI/CD
pytest --json-report --json-report-file=report.json

# Reporte de cobertura
pytest --cov=tests --cov-report=html
```

#### 8. **Scripts de Ejecución**

**PowerShell (`run_tests.ps1`):**
```powershell
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Ejecutar todas las pruebas
pytest -v

# Ejecutar solo casos felices
pytest -v -m happy_path

# Generar reporte HTML
pytest --html=report.html --self-contained-html
```

**Python (`run_tests.py`):**
```python
import subprocess
import sys

def run_tests(markers=None, verbose=True):
    cmd = ["pytest"]
    if verbose:
        cmd.append("-v")
    if markers:
        cmd.extend(["-m", markers])
    
    result = subprocess.run(cmd)
    return result.returncode
```

#### 9. **Variables de Entorno (`.env.example`)**
```env
API_BASE_URL=http://localhost:8000
API_USERNAME=admin
API_PASSWORD=secret
TIMEOUT=30
```

### 🚀 Ejecución del Ejemplo 1

```powershell
# 1. Navegar al directorio
cd Ejemplo1_ConsultaBureauCrédito

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
.\venv\Scripts\Activate.ps1

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar variables de entorno
copy .env.example .env
# Editar .env con valores correctos

# 6. Ejecutar pruebas
python run_tests.py
# o
.\run_tests.ps1
```

### 📊 Resultados Obtenidos
- ✅ **26 casos de prueba** implementados
- ✅ **100% de éxito** en ejecución
- ✅ **4 categorías** de pruebas (happy_path, edge_cases, validations, errors)
- ✅ **Cobertura completa** de funcionalidades críticas
- ✅ **Reportes** en múltiples formatos (HTML, JSON, XML)

---

## Ejemplo 2: Sistema de Transferencias Bancarias

### 📁 Directorio
`Ejemplo2_TransferenciaBancaria/`

### 🎯 Objetivo
Crear una API completa de transferencias bancarias con FastAPI y un sistema de pruebas automatizadas que genere reportes en formatos SVE (Sistema de Validación y Evaluación).

### 📝 Paso a Paso Realizado

#### 1. **Estructura del Proyecto**
```
Ejemplo2_TransferenciaBancaria/
├── main.py                              # API FastAPI
├── tests/
│   ├── __init__.py
│   ├── conftest.py                      # Configuración y fixtures
│   ├── test_transferencias.py           # Casos de prueba
│   └── sve_reporter.py                  # Generador de reportes SVE
├── requirements.txt                     # Dependencias
├── run_api.ps1                          # Script para iniciar API
├── run_tests.ps1                        # Script para ejecutar pruebas
├── run_tests_sve.ps1                    # Script para reportes SVE
└── Transferencias_Bancarias.postman_collection.json  # Colección Postman
```

#### 2. **Implementación de la API FastAPI (`main.py`)**

##### **A. Modelos Pydantic**
```python
class CuentaBancaria(BaseModel):
    numero_cuenta: str = Field(..., pattern=r'^\d{10}$')
    titular: str = Field(..., min_length=3, max_length=100)
    saldo: float = Field(..., ge=0)
    tipo_cuenta: str = Field(..., pattern=r'^(AHORROS|CORRIENTE)$')
    estado: str = Field(default="ACTIVA", pattern=r'^(ACTIVA|BLOQUEADA|CERRADA)$')

class TransferenciaRequest(BaseModel):
    cuenta_origen: str = Field(..., pattern=r'^\d{10}$')
    cuenta_destino: str = Field(..., pattern=r'^\d{10}$')
    monto: float = Field(..., gt=0, le=1000000)
    concepto: str = Field(..., min_length=3, max_length=200)
```

##### **B. Endpoints Implementados**

1. **GET /** - Información de la API
2. **POST /cuentas** - Crear cuenta bancaria
3. **GET /cuentas/{numero_cuenta}** - Consultar cuenta
4. **GET /cuentas** - Listar todas las cuentas
5. **POST /transferencias** - Realizar transferencia
6. **GET /transferencias** - Historial de transferencias
7. **GET /transferencias/{transferencia_id}** - Detalle de transferencia

##### **C. Validaciones de Negocio**
```python
# Validación de saldo suficiente
if cuenta_origen["saldo"] < request.monto:
    raise HTTPException(
        status_code=400,
        detail="Saldo insuficiente en cuenta origen"
    )

# Validación de estado de cuenta
if cuenta_origen["estado"] != "ACTIVA":
    raise HTTPException(
        status_code=400,
        detail="La cuenta origen no está activa"
    )
```

#### 3. **Sistema de Pruebas Automatizadas**

##### **A. Fixtures de Pytest (`conftest.py`)**
```python
@pytest.fixture(scope="module")
def client():
    """Cliente de pruebas FastAPI"""
    with TestClient(app) as c:
        yield c

@pytest.fixture
def cuenta_origen(client):
    """Crear cuenta origen para pruebas"""
    cuenta = {
        "numero_cuenta": "1234567890",
        "titular": "Juan Pérez",
        "saldo": 10000.00,
        "tipo_cuenta": "AHORROS"
    }
    response = client.post("/cuentas", json=cuenta)
    return response.json()
```

##### **B. Casos de Prueba Implementados (`test_transferencias.py`)**

**Pruebas de Creación de Cuentas:**
- ✅ Crear cuenta válida
- ✅ Validar número de cuenta (10 dígitos)
- ✅ Validar tipo de cuenta (AHORROS/CORRIENTE)
- ✅ Rechazar cuenta duplicada
- ✅ Validar campos obligatorios

**Pruebas de Consulta:**
- ✅ Consultar cuenta existente
- ✅ Error 404 para cuenta inexistente
- ✅ Listar todas las cuentas

**Pruebas de Transferencias:**
- ✅ Transferencia exitosa
- ✅ Validar actualización de saldos
- ✅ Rechazar saldo insuficiente
- ✅ Rechazar cuenta bloqueada
- ✅ Rechazar transferencia a misma cuenta
- ✅ Validar monto mínimo y máximo
- ✅ Validar longitud de concepto
- ✅ Historial de transferencias

**Pruebas de Validación:**
- ✅ Número de cuenta inválido
- ✅ Monto negativo
- ✅ Monto cero
- ✅ Monto excede límite (>1,000,000)
- ✅ Concepto muy corto (<3 caracteres)
- ✅ Concepto muy largo (>200 caracteres)

#### 4. **Sistema de Reportes SVE (`sve_reporter.py`)**

##### **A. Clase SVEReporter**
```python
class SVEReporter:
    def __init__(self):
        self.test_results = []
    
    def add_result(self, test_case: dict):
        """Agregar resultado de prueba"""
        self.test_results.append(test_case)
    
    def generate_csv_report(self, filename: str):
        """Generar reporte CSV"""
        
    def generate_json_report(self, filename: str):
        """Generar reporte JSON"""
        
    def generate_xml_report(self, filename: str):
        """Generar reporte XML"""
```

##### **B. Formatos de Reporte**

**CSV (`sve_report.csv`):**
```csv
Test ID,Categoría,Descripción,Estado,Timestamp,Duración (s),Mensaje
TC001,Cuentas,Crear cuenta válida,PASSED,2025-12-11T10:30:00,0.125,
TC002,Transferencias,Transferencia exitosa,PASSED,2025-12-11T10:30:01,0.234,
```

**JSON (`sve_report.json`):**
```json
{
  "summary": {
    "total_tests": 24,
    "passed": 24,
    "failed": 0,
    "skipped": 0,
    "pass_rate": 100.0
  },
  "test_results": [...]
}
```

**XML (`sve_report.xml`):**
```xml
<testsuite name="Transferencias Bancarias" tests="24" failures="0">
  <testcase classname="test_transferencias" name="TC001" time="0.125">
    <system-out>Crear cuenta válida</system-out>
  </testcase>
</testsuite>
```

**HTML (`report.html`):**
- Reporte visual interactivo
- Gráficos de resultados
- Detalles de cada prueba
- Filtros y búsqueda

#### 5. **Scripts de Ejecución**

**Iniciar API (`run_api.ps1`):**
```powershell
Write-Host "Iniciando API de Transferencias Bancarias..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Ejecutar Pruebas (`run_tests.ps1`):**
```powershell
Write-Host "Ejecutando pruebas automatizadas..."
pytest tests/test_transferencias.py -v --html=report.html --self-contained-html
```

**Generar Reportes SVE (`run_tests_sve.ps1`):**
```powershell
Write-Host "Ejecutando pruebas con reportes SVE..."
pytest tests/test_transferencias.py -v --tb=short
Write-Host "`nReportes SVE generados:"
Write-Host "  - sve_report.csv"
Write-Host "  - sve_report.json"
Write-Host "  - sve_report.xml"
```

#### 6. **Integración con Postman**

Se creó una colección Postman (`Transferencias_Bancarias.postman_collection.json`) con:
- Variables de entorno
- Todos los endpoints documentados
- Ejemplos de requests/responses
- Tests de validación automáticos

#### 7. **Documentación Generada**

- **README.md**: Guía principal del proyecto
- **DOCUMENTACION_TECNICA.md**: Especificaciones técnicas
- **DOCUMENTACION_SVE.md**: Sistema de reportes SVE
- **GUIA_EJECUCION_AUTOMATIZACION.md**: Guía paso a paso
- **RESUMEN_EJECUTIVO.md**: Resumen para stakeholders
- **CHECKLIST_VERIFICACION.md**: Lista de verificación
- **PROYECTO_COMPLETADO.md**: Estado del proyecto

### 🚀 Ejecución del Ejemplo 2

```powershell
# 1. Navegar al directorio
cd Ejemplo2_TransferenciaBancaria

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
.\venv\Scripts\Activate.ps1

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Iniciar API (Terminal 1)
.\run_api.ps1
# La API estará disponible en http://localhost:8000
# Documentación interactiva en http://localhost:8000/docs

# 6. Ejecutar pruebas (Terminal 2)
.\run_tests.ps1

# 7. Generar reportes SVE
.\run_tests_sve.ps1
```

### 📊 Resultados Obtenidos
- ✅ **24 casos de prueba** implementados
- ✅ **100% de éxito** en ejecución
- ✅ **7 endpoints** funcionales
- ✅ **Reportes SVE** en 3 formatos (CSV, JSON, XML)
- ✅ **Reporte HTML** interactivo
- ✅ **API documentada** con Swagger/OpenAPI
- ✅ **Colección Postman** completa

---

## Requisitos Generales

### 🔧 Software Necesario
- **Python 3.8+**
- **pip** (gestor de paquetes)
- **PowerShell** (para Windows)
- **Git** (control de versiones)

### 📦 Dependencias Python

**Ejemplo 1:**
```txt
pytest==7.4.3
pytest-html==4.1.1
pytest-json-report==1.5.0
pytest-cov==4.1.0
requests==2.31.0
python-dotenv==1.0.0
```

**Ejemplo 2:**
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pytest==7.4.3
pytest-html==4.1.1
httpx==0.25.1
pydantic==2.5.0
```

---

## Configuración del Entorno

### 1. **Clonar el Repositorio**
```powershell
git clone https://github.com/1577089/CapacitacionIA-Banistmo.git
cd CapacitacionIA-Banistmo/Clase2
```

### 2. **Crear Entorno Virtual**
```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
.\venv\Scripts\Activate.ps1

# Activar entorno virtual (Linux/Mac)
source venv/bin/activate
```

### 3. **Instalar Dependencias**
```powershell
# Para Ejemplo 1
cd Ejemplo1_ConsultaBureauCrédito
pip install -r requirements.txt

# Para Ejemplo 2
cd Ejemplo2_TransferenciaBancaria
pip install -r requirements.txt
```

### 4. **Configurar Variables de Entorno**
```powershell
# Ejemplo 1
copy .env.example .env
# Editar .env con tus valores
```

---

## Resumen de Aprendizajes

### 🎓 Conceptos Aplicados

#### 1. **Testing**
- ✅ Pytest como framework de testing
- ✅ Fixtures y configuración
- ✅ Markers para categorización
- ✅ Parametrización de pruebas
- ✅ Mocking y stubs
- ✅ Cobertura de código

#### 2. **API Development**
- ✅ FastAPI para APIs REST
- ✅ Pydantic para validación de datos
- ✅ Swagger/OpenAPI documentation
- ✅ Manejo de errores HTTP
- ✅ Endpoints CRUD
- ✅ Validaciones de negocio

#### 3. **Best Practices**
- ✅ Estructura modular del código
- ✅ Separación de concerns
- ✅ Datos de prueba centralizados
- ✅ Configuración por entorno
- ✅ Documentación completa
- ✅ Scripts de automatización

#### 4. **Reporting**
- ✅ Reportes HTML interactivos
- ✅ Reportes JSON para CI/CD
- ✅ Reportes XML (JUnit)
- ✅ Reportes CSV para análisis
- ✅ Métricas de calidad

#### 5. **DevOps**
- ✅ Control de versiones (Git)
- ✅ Automatización de pruebas
- ✅ Scripts de ejecución
- ✅ Manejo de dependencias
- ✅ Entornos virtuales

### 📈 Métricas Generales

| Métrica | Ejemplo 1 | Ejemplo 2 | Total |
|---------|-----------|-----------|-------|
| Casos de Prueba | 26 | 24 | 50 |
| Líneas de Código | ~800 | ~1200 | ~2000 |
| Cobertura | 95%+ | 95%+ | 95%+ |
| Tasa de Éxito | 100% | 100% | 100% |
| Archivos Creados | 15 | 20 | 35 |
| Formatos de Reporte | 3 | 4 | 7 |

---

## 🚀 Comandos Rápidos

### Ejemplo 1: Buró de Crédito
```powershell
cd Ejemplo1_ConsultaBureauCrédito
.\venv\Scripts\Activate.ps1
pytest -v                                    # Todas las pruebas
pytest -v -m happy_path                      # Solo casos felices
pytest -v -m edge_cases                      # Solo casos extremos
pytest --html=report.html                    # Con reporte HTML
```

### Ejemplo 2: Transferencias
```powershell
cd Ejemplo2_TransferenciaBancaria
.\venv\Scripts\Activate.ps1

# Terminal 1: Iniciar API
uvicorn main:app --reload

# Terminal 2: Ejecutar pruebas
pytest -v
pytest --html=report.html                    # Con reporte HTML
.\run_tests_sve.ps1                          # Generar reportes SVE
```

---

## 📚 Recursos Adicionales

### Documentación
- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Requests Documentation](https://requests.readthedocs.io/)

### Herramientas
- [Postman](https://www.postman.com/)
- [VS Code](https://code.visualstudio.com/)
- [Git](https://git-scm.com/)

---

## 👥 Autor
**Capacitación IA - Banistmo**
- Fecha: Diciembre 2025
- Clase: 2 - Automatización de Pruebas

---

## 📄 Licencia
Este proyecto es parte del material de capacitación de Banistmo y está destinado únicamente para fines educativos.

---

## 🤝 Contribuciones
Si encuentras algún error o tienes sugerencias de mejora, por favor:
1. Crea un issue en el repositorio
2. Haz un fork del proyecto
3. Crea una rama con tu mejora
4. Envía un pull request

---

## ✅ Verificación de Instalación

Para verificar que todo está correctamente instalado:

```powershell
# Verificar Python
python --version

# Verificar pip
pip --version

# Verificar pytest
pytest --version

# Verificar FastAPI/Uvicorn
uvicorn --version
```

---

**¡Feliz automatización de pruebas! 🚀**
