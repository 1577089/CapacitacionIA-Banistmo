# 🏦 API de Transferencias Bancarias - Testing QA

Sistema completo de pruebas automatizadas para transferencias bancarias con validaciones de límites, seguridad y reglas de negocio.

## 🎯 Características

- ✅ **15 casos de prueba automatizados** (pytest)
- ✅ **API REST completa** (FastAPI + Uvicorn)
- ✅ **Colección Postman** exportable
- ✅ **Reportes HTML** de tests y cobertura
- ✅ **Documentación técnica** completa

## 📋 Reglas de Negocio Implementadas

| Validación | Valor | Comportamiento |
|------------|-------|----------------|
| **Límite Diario** | $50,000 | Rechaza transferencias que excedan acumulado diario |
| **Límite Mensual** | $5,000,000 | Rechaza transferencias que excedan acumulado mensual |
| **OTP Obligatorio** | > $1,000,000 | Requiere código OTP válido (123456 en testing) |
| **Mantenimiento** | 1:00-3:00 AM | Sistema no disponible en ventana de mantenimiento |
| **Rate Limiting** | 10 req/min | Protección contra alta frecuencia |

## 🚀 Quick Start

### 1. Instalar dependencias

```powershell
python -m pip install -r requirements.txt
```

### 2. Iniciar API

```powershell
# Opción A: Script directo
python main.py

# Opción B: PowerShell script
.\run_api.ps1
```

La API estará en: **http://localhost:8000**  
Documentación: **http://localhost:8000/docs**

### 3. Ejecutar tests

```powershell
# Configurar token
$env:AUTH_TOKEN="Bearer test"

# Ejecutar suite completa
pytest -v

# Con reportes HTML
pytest --cov=main --cov-report=html --html=report.html --self-contained-html -v
```

## 📊 Resultados de Tests

```
✅ 13 PASSED
⏭️  2 SKIPPED (requieren config específica)
⏱️  Duración: ~80 segundos
```

### Tests Incluidos

1. ✅ Path feliz - Transferencia exitosa
2. ✅ Excede límite diario ($60K > $50K)
3. ✅ Excede límite mensual
4. ✅ Saldo insuficiente
5. ✅ OTP inválido para montos > $1M
6. ⏭️ Transferencia en mantenimiento (requiere `FORCE_MAINTENANCE=1`)
7. ✅ Cuenta destino inválida
8. ✅ Edge: Transferencia $0.01
9. ✅ Edge: Monto negativo
10. ✅ Edge: Decimales excesivos
11. ✅ Concurrencia (race conditions)
12. ⏭️ Cuenta bloqueada (requiere `BLOCKED_ACCOUNT`)
13. ✅ Origen = Destino
14. ✅ Rate limiting
15. ✅ Sin autenticación

## 📡 Endpoints Principales

### POST /api/transferencias
Crear transferencia bancaria

**Request:**
```json
{
  "origen": "12345678",
  "destino": "87654321",
  "monto": 1000,
  "otp": "123456"  // Opcional
}
```

**Headers:**
```
Content-Type: application/json
Authorization: Bearer {token}
X-OTP: {codigo}  // Opcional, alternativa a campo otp
```

### GET /health
Verificar estado del servicio

### GET /api/transferencias/historial
Obtener historial de transferencias

### GET /api/cuentas/{numero}
Consultar estado de cuenta

### POST /api/cuentas/{numero}/reset
Reset de cuenta para testing

## 📦 Colección Postman

Importar archivo: `Transferencias_Bancarias.postman_collection.json`

Incluye:
- 14 requests pre-configurados
- Assertions automáticas
- Variables de entorno
- Tests de validación

## 📚 Documentación

- **[DOCUMENTACION_TECNICA.md](./DOCUMENTACION_TECNICA.md)** - Guía completa
  - Arquitectura
  - Especificaciones API
  - Matriz de casos de prueba
  - Troubleshooting
  - Configuración de producción

## 🔧 Variables de Entorno

```powershell
# Configuración de API
$env:BASE_URL = "http://localhost:8000"
$env:TRANSFER_ENDPOINT = "/api/transferencias"

# Autenticación
$env:AUTH_TOKEN = "Bearer test_token"

# Cuentas de prueba
$env:SRC_ACCOUNT = "12345678"
$env:DST_ACCOUNT = "87654321"
$env:BLOCKED_ACCOUNT = "99999999"

# Flags especiales
$env:FORCE_MAINTENANCE = "1"  # Simular mantenimiento
```

## 📈 Reportes

Después de ejecutar tests con reportes:

- **Tests HTML**: `report.html`
- **Cobertura**: `htmlcov/index.html`

Abrir en navegador:
```powershell
Start-Process report.html
Start-Process htmlcov/index.html
```

## 🛠️ Estructura del Proyecto

```
.
├── main.py                          # API FastAPI
├── tests/
│   ├── __init__.py
│   └── test_transferencias.py       # 15 tests automatizados
├── requirements.txt                 # Dependencias
├── README.md                        # Este archivo
├── DOCUMENTACION_TECNICA.md         # Guía técnica completa
├── Transferencias_Bancarias.postman_collection.json
├── run_api.ps1                      # Script iniciar API
├── run_tests.ps1                    # Script ejecutar tests
└── htmlcov/                         # Reporte cobertura (generado)
```

## 🐛 Troubleshooting

### Tests se saltan (SKIPPED)
```powershell
# Verificar que API esté corriendo
curl http://localhost:8000/health

# Reiniciar API si es necesario
python main.py
```

### Puerto 8000 ocupado
```powershell
# Detener procesos Python
Get-Process -Name python | Stop-Process -Force

# Reiniciar
python main.py
```

### Límite diario agotado
```powershell
# Reset cuenta antes de tests
curl -X POST http://localhost:8000/api/cuentas/12345678/reset
```

## 📝 Tecnologías

- **Python** 3.8+
- **FastAPI** - Framework web moderno
- **Uvicorn** - Servidor ASGI
- **Pydantic** - Validación de datos
- **pytest** - Testing framework
- **pytest-cov** - Cobertura de código
- **pytest-html** - Reportes HTML
- **requests** - HTTP client para tests

## 🔐 Seguridad

⚠️ **Este código es para TESTING/DEMO**.

Para producción implementar:
- Base de datos real (PostgreSQL/MySQL)
- JWT con firma y expiración
- OTP dinámico (Twilio/SendGrid)
- HTTPS con certificados
- Secrets en vault
- Logging robusto

## 📞 Contacto

Para dudas sobre los tests o la API:
1. Revisar `/docs` (Swagger UI)
2. Consultar `DOCUMENTACION_TECNICA.md`
3. Verificar logs en consola

---

**Versión**: 1.0.0  
**Última actualización**: 2025-12-10  
**Autor**: QA Senior - Banca Digital