# 📚 Documentación Técnica - API de Transferencias Bancarias

## 📋 Tabla de Contenidos
- [Introducción](#introducción)
- [Arquitectura](#arquitectura)
- [Especificaciones de la API](#especificaciones-de-la-api)
- [Casos de Prueba](#casos-de-prueba)
- [Instalación y Configuración](#instalación-y-configuración)
- [Ejecución](#ejecución)
- [Reportes](#reportes)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Introducción

Este proyecto implementa una **API REST de transferencias bancarias** con validaciones completas de seguridad, límites y reglas de negocio, diseñada para ejercicios prácticos de QA en banca digital.

### Características Principales

✅ **Validaciones de Negocio**
- Límite diario: $50,000
- Límite mensual: $5,000,000
- OTP obligatorio para montos > $1,000,000
- Ventana de mantenimiento: 1:00 AM - 3:00 AM

✅ **Seguridad**
- Autenticación mediante Bearer Token
- Rate limiting (10 operaciones/minuto)
- Validación de OTP para transacciones de alto valor
- Transacciones atómicas con locks

✅ **Validaciones Técnicas**
- Cuenta origen != cuenta destino
- Cuentas existentes y activas
- Saldo suficiente
- Formato de montos (máx. 2 decimales)
- Montos positivos

---

## 🏗️ Arquitectura

### Stack Tecnológico

- **Framework**: FastAPI 0.115+
- **Server**: Uvicorn (ASGI)
- **Validación**: Pydantic v2
- **Testing**: pytest + pytest-cov + pytest-html
- **Python**: 3.8+

### Estructura del Proyecto

```
Ejemplo2_TransferenciaBancaria/
├── main.py                                    # API FastAPI principal
├── tests/
│   ├── __init__.py
│   └── test_transferencias.py                 # 15 casos de prueba automatizados
├── requirements.txt                           # Dependencias
├── README.md                                  # Instrucciones básicas
├── DOCUMENTACION_TECNICA.md                   # Este archivo
├── Transferencias_Bancarias.postman_collection.json
├── run_api.ps1                                # Script para iniciar API
├── run_tests.ps1                              # Script para ejecutar tests
├── report.html                                # Reporte HTML de tests
└── htmlcov/                                   # Reporte de cobertura HTML
```

---

## 📡 Especificaciones de la API

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
```http
GET /health
```

**Response 200:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-10T12:00:00.000000"
}
```

---

#### 2. Crear Transferencia
```http
POST /api/transferencias
Content-Type: application/json
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "origen": "12345678",
  "destino": "87654321",
  "monto": 1000.00,
  "otp": "123456"  // Opcional, requerido si monto > $1,000,000
}
```

**Headers opcionales:**
- `X-OTP`: Código OTP (alternativa al campo en body)
- `X-Force-Maintenance`: "1" para simular mantenimiento (solo testing)

**Response 200:**
```json
{
  "id": 1,
  "origen": "12345678",
  "destino": "87654321",
  "monto": 1000.0,
  "status": "COMPLETED",
  "fecha": "2025-12-10T12:00:00.123456",
  "mensaje": "Transferencia realizada exitosamente",
  "saldo_restante": 99000.0
}
```

**Errores Posibles:**

| Código | Descripción |
|--------|-------------|
| 400 | Validación fallida (origen=destino, formato inválido) |
| 401 | Token ausente/inválido, OTP inválido |
| 402 | Saldo insuficiente |
| 403 | Límite diario/mensual excedido, cuenta bloqueada |
| 404 | Cuenta no encontrada |
| 422 | Error de validación Pydantic (monto negativo, decimales) |
| 429 | Rate limit excedido |
| 503 | Sistema en mantenimiento |

---

#### 3. Obtener Historial
```http
GET /api/transferencias/historial
```

**Response 200:**
```json
{
  "transferencias": [
    {
      "id": 1,
      "origen": "12345678",
      "destino": "87654321",
      "monto": 1000.0,
      "fecha": "2025-12-10T12:00:00.123456",
      "status": "COMPLETED"
    }
  ],
  "total": 1
}
```

---

#### 4. Obtener Estado de Cuenta
```http
GET /api/cuentas/{numero_cuenta}
```

**Response 200:**
```json
{
  "numero": "12345678",
  "saldo": 100000.0,
  "estado": "ACTIVA",
  "transferido_hoy": 0,
  "transferido_mes": 0
}
```

---

#### 5. Reset Cuenta (Solo Testing)
```http
POST /api/cuentas/{numero_cuenta}/reset
```

**Response 200:**
```json
{
  "mensaje": "Cuenta reseteada",
  "cuenta": {
    "saldo": 100000,
    "estado": "ACTIVA",
    "transferido_hoy": 0,
    "transferido_mes": 0
  }
}
```

---

## 🧪 Casos de Prueba

### Suite Completa (15 Tests)

| ID | Nombre | Descripción | Resultado Esperado |
|----|--------|-------------|-------------------|
| 01 | Path Feliz | Transferencia exitosa $1,000 | HTTP 200/201, status=COMPLETED |
| 02 | Límite Diario | Transferir $60,000 (>$50K) | HTTP 400/403, mensaje límite |
| 03 | Límite Mensual | Transferir $100,000 con mes agotado | HTTP 400/403 |
| 04 | Saldo Insuficiente | Transferir $1,000,000,000 | HTTP 402, mensaje saldo |
| 05 | OTP Inválido | $2M con OTP="000000" | HTTP 401, mensaje OTP |
| 06 | Mantenimiento | Header X-Force-Maintenance=1 | HTTP 503/423 |
| 07 | Cuenta Destino Inválida | Destino="00000000" | HTTP 404, cuenta no encontrada |
| 08 | Edge: $0.01 | Monto mínimo | HTTP 200/201 o 400 |
| 09 | Edge: Negativo | Monto=-100 | HTTP 422 (Pydantic) |
| 10 | Edge: Decimales | Monto=100.123456 | HTTP 422 o redondeo |
| 11 | Concurrencia | 2 transferencias $30K simultáneas | Una pasa, otra falla |
| 12 | Cuenta Bloqueada | Origen="99999999" (bloqueada) | HTTP 403 |
| 13 | Origen=Destino | Misma cuenta | HTTP 400 |
| 14 | Rate Limiting | 10 transferencias en <60s | HTTP 429 después de 10 |
| 15 | Sin Token | Sin header Authorization | HTTP 401 |

### Matriz de Cobertura

| Categoría | Tests | Cobertura |
|-----------|-------|-----------|
| Validaciones de Negocio | 5 | Límites, OTP, mantenimiento |
| Validaciones de Datos | 4 | Cuentas, montos, formato |
| Edge Cases | 3 | Valores extremos |
| Seguridad | 2 | Auth, rate limiting |
| Concurrencia | 1 | Race conditions |
| **TOTAL** | **15** | **100%** |

---

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes)
- PowerShell (Windows) o bash (Linux/Mac)

### Paso 1: Instalar Dependencias

```powershell
# PowerShell
python -m pip install -r requirements.txt
```

```bash
# Linux/Mac
python3 -m pip install -r requirements.txt
```

### Paso 2: Configurar Variables de Entorno (Opcional)

```powershell
# PowerShell
$env:BASE_URL = "http://localhost:8000"
$env:AUTH_TOKEN = "Bearer mi_token_personalizado"
$env:TRANSFER_ENDPOINT = "/api/transferencias"
```

```bash
# Linux/Mac
export BASE_URL="http://localhost:8000"
export AUTH_TOKEN="Bearer mi_token_personalizado"
export TRANSFER_ENDPOINT="/api/transferencias"
```

---

## ▶️ Ejecución

### Iniciar API

**Opción 1: Script PowerShell**
```powershell
.\run_api.ps1
```

**Opción 2: Comando directo**
```powershell
python main.py
```

**Opción 3: Uvicorn con reload**
```powershell
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en:
- **API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

### Ejecutar Tests

**Opción 1: Script PowerShell**
```powershell
.\run_tests.ps1
```

**Opción 2: pytest básico**
```powershell
$env:AUTH_TOKEN="Bearer test"
pytest -v
```

**Opción 3: Con cobertura y reportes HTML**
```powershell
$env:AUTH_TOKEN="Bearer test"
pytest --cov=main --cov-report=html --html=report.html --self-contained-html -v
```

**Opción 4: Test específico**
```powershell
$env:AUTH_TOKEN="Bearer test"
pytest tests/test_transferencias.py::test_01_transferencia_exitosa_path_feliz -v
```

---

## 📊 Reportes

### Reporte HTML de Tests

Después de ejecutar los tests con `--html`, abrir:
```
file:///C:/ruta/al/proyecto/report.html
```

Contiene:
- ✅ Estado de cada test (PASSED/FAILED/SKIPPED)
- ⏱️ Tiempo de ejecución
- 📝 Logs y errores detallados
- 📈 Gráficos de resumen

### Reporte de Cobertura

Después de ejecutar con `--cov-report=html`, abrir:
```
file:///C:/ruta/al/proyecto/htmlcov/index.html
```

Muestra:
- % de líneas cubiertas por módulo
- Líneas no ejecutadas (resaltadas en rojo)
- Branches y paths de ejecución

---

## 🔧 Troubleshooting

### Problema: Tests se saltan (SKIPPED)

**Causa**: API no está corriendo o endpoint no responde.

**Solución**:
```powershell
# Verificar que API esté corriendo
curl http://localhost:8000/health

# Si no responde, iniciar API
python main.py
```

---

### Problema: Error "Port 8000 already in use"

**Causa**: Otro proceso usa el puerto 8000.

**Solución**:
```powershell
# Opción 1: Detener procesos Python
Get-Process -Name python | Stop-Process -Force

# Opción 2: Usar otro puerto
python -m uvicorn main:app --port 8001
# Actualizar BASE_URL en tests
$env:BASE_URL="http://localhost:8001"
```

---

### Problema: Todos los tests fallan por límite diario

**Causa**: Cuenta de prueba ya alcanzó límite diario.

**Solución**:
```powershell
# Reset cuenta antes de ejecutar tests
curl -X POST http://localhost:8000/api/cuentas/12345678/reset
pytest -v
```

---

### Problema: Test de concurrencia falla

**Causa**: Lock no está funcionando o montos no están ajustados.

**Solución**:
1. Verificar que `threading.Lock()` esté en `main.py`
2. Ajustar montos de prueba en test_11:
```python
amt = 30000  # 30K + 30K = 60K > límite diario 50K
```

---

### Problema: Coverage no muestra datos

**Causa**: Módulo `main` no fue importado durante tests.

**Solución**:
```powershell
# Ejecutar tests de forma que importen main
pytest --cov=. --cov-report=html -v
```

---

## 📦 Colección Postman

### Importar en Postman

1. Abrir Postman
2. Click en **Import**
3. Seleccionar archivo: `Transferencias_Bancarias.postman_collection.json`
4. La colección incluye:
   - 14 requests pre-configurados
   - Variables de entorno
   - Tests automáticos (assertions)

### Variables de Colección

- `base_url`: http://localhost:8000
- `auth_token`: Bearer test_token_123
- `cuenta_origen`: 12345678
- `cuenta_destino`: 87654321
- `otp_valido`: 123456

### Ejecutar Colección Completa

1. Click derecho en la colección
2. **Run collection**
3. Ajustar orden si necesario
4. Click **Run Transferencias Bancarias**

---

## 🔐 Seguridad

### Configuración de Producción

⚠️ **Este código es para TESTING/DEMO únicamente**. Para producción:

1. **Base de datos real**: Reemplazar diccionario en memoria por PostgreSQL/MySQL
2. **OTP dinámico**: Integrar con servicio SMS/email (Twilio, SendGrid)
3. **JWT real**: Implementar auth con tokens firmados y expiración
4. **HTTPS**: Usar certificados SSL/TLS
5. **Rate limiting robusto**: Redis + middleware
6. **Logging**: Winston/structlog para auditoría
7. **Secrets**: Usar variables de entorno o vault (HashiCorp, AWS Secrets)

### Variables Sensibles

```powershell
# NO commitear en Git
$env:DATABASE_URL = "postgresql://user:pass@host/db"
$env:JWT_SECRET = "clave_secreta_fuerte_aqui"
$env:OTP_SERVICE_KEY = "twilio_api_key"
```

---

## 📞 Soporte

Para dudas o issues:
- Revisar logs en consola
- Consultar `/docs` (Swagger UI)
- Verificar variables de entorno
- Ejecutar health check: `curl http://localhost:8000/health`

---

## 📝 Changelog

### v1.0.0 (2025-12-10)
- ✅ Implementación inicial API FastAPI
- ✅ 15 casos de prueba automatizados
- ✅ Validaciones de límites y OTP
- ✅ Rate limiting
- ✅ Transacciones atómicas con locks
- ✅ Colección Postman
- ✅ Reportes HTML

---

**Última actualización**: 2025-12-10  
**Autor**: QA Senior - Banca Digital  
**Versión**: 1.0.0
