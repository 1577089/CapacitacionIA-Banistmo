# ✅ CHECKLIST DE VERIFICACIÓN - Proyecto Transferencias Bancarias

Use este checklist para verificar que todo el proyecto está funcionando correctamente.

---

## 📋 Pre-requisitos

- [ ] Python 3.8+ instalado
  ```powershell
  python --version
  ```

- [ ] pip actualizado
  ```powershell
  python -m pip --version
  ```

- [ ] PowerShell disponible (Windows)
  ```powershell
  $PSVersionTable.PSVersion
  ```

---

## 🔧 Instalación

- [ ] Dependencias instaladas sin errores
  ```powershell
  python -m pip install -r requirements.txt
  ```

- [ ] Verificar paquetes instalados
  ```powershell
  pip list | Select-String "fastapi|pytest|uvicorn|requests|pydantic"
  ```

  **Esperado**: Ver versiones de fastapi, pytest, pytest-cov, pytest-html, uvicorn, requests, pydantic

---

## 🚀 API - Verificación

- [ ] API inicia sin errores
  ```powershell
  python main.py
  ```
  
  **Esperado**: Ver mensajes:
  ```
  INFO:     Started server process
  INFO:     Application startup complete.
  INFO:     Uvicorn running on http://0.0.0.0:8000
  ```

- [ ] Health check responde
  ```powershell
  curl http://localhost:8000/health
  ```
  
  **Esperado**: HTTP 200, JSON con `{"status":"healthy",...}`

- [ ] Swagger UI accesible
  ```powershell
  Start-Process http://localhost:8000/docs
  ```
  
  **Esperado**: Página web con documentación interactiva

- [ ] Root endpoint responde
  ```powershell
  curl http://localhost:8000/
  ```
  
  **Esperado**: HTTP 200, mensaje de bienvenida

---

## 🧪 Tests - Verificación

- [ ] Tests se ejecutan sin errores de configuración
  ```powershell
  $env:AUTH_TOKEN="Bearer test"
  pytest --collect-only
  ```
  
  **Esperado**: Ver lista de 15 tests recolectados

- [ ] Suite completa ejecuta correctamente
  ```powershell
  $env:AUTH_TOKEN="Bearer test"
  pytest -v
  ```
  
  **Esperado**: 
  - 13 PASSED
  - 2 SKIPPED
  - 0 FAILED
  - Duración: 60-90 segundos

- [ ] Test específico funciona
  ```powershell
  $env:AUTH_TOKEN="Bearer test"
  pytest tests/test_transferencias.py::test_01_transferencia_exitosa_path_feliz -v
  ```
  
  **Esperado**: 1 PASSED

---

## 📊 Reportes - Verificación

- [ ] Reporte HTML se genera
  ```powershell
  $env:AUTH_TOKEN="Bearer test"
  pytest --html=report.html --self-contained-html
  ```
  
  **Esperado**: Archivo `report.html` creado

- [ ] Reporte HTML se abre en navegador
  ```powershell
  Start-Process report.html
  ```
  
  **Esperado**: Página HTML con resultados de tests

- [ ] Reporte de cobertura se genera
  ```powershell
  $env:AUTH_TOKEN="Bearer test"
  pytest --cov=main --cov-report=html
  ```
  
  **Esperado**: Carpeta `htmlcov/` creada

- [ ] Reporte de cobertura se abre
  ```powershell
  Start-Process htmlcov/index.html
  ```
  
  **Esperado**: Página HTML con métricas de cobertura

---

## 🔗 Endpoints - Verificación Funcional

### Endpoint: POST /api/transferencias (Path Feliz)

- [ ] Transferencia exitosa
  ```powershell
  $body = @{origen="12345678";destino="87654321";monto=1000} | ConvertTo-Json
  Invoke-WebRequest -Uri "http://localhost:8000/api/transferencias" -Method POST -Body $body -Headers @{"Content-Type"="application/json";"Authorization"="Bearer test"} -UseBasicParsing
  ```
  
  **Esperado**: HTTP 200/201, JSON con `"status":"COMPLETED"`

### Endpoint: POST /api/transferencias (Límite Diario)

- [ ] Rechazo por límite diario
  ```powershell
  $body = @{origen="12345678";destino="87654321";monto=60000} | ConvertTo-Json
  Invoke-WebRequest -Uri "http://localhost:8000/api/transferencias" -Method POST -Body $body -Headers @{"Content-Type"="application/json";"Authorization"="Bearer test"} -UseBasicParsing
  ```
  
  **Esperado**: HTTP 403, mensaje "Excede límite diario"

### Endpoint: POST /api/transferencias (Sin Auth)

- [ ] Rechazo sin token
  ```powershell
  $body = @{origen="12345678";destino="87654321";monto=100} | ConvertTo-Json
  Invoke-WebRequest -Uri "http://localhost:8000/api/transferencias" -Method POST -Body $body -Headers @{"Content-Type"="application/json"} -UseBasicParsing
  ```
  
  **Esperado**: HTTP 401, mensaje "No autorizado"

### Endpoint: GET /api/transferencias/historial

- [ ] Historial accesible
  ```powershell
  Invoke-WebRequest -Uri "http://localhost:8000/api/transferencias/historial" -UseBasicParsing | ConvertFrom-Json
  ```
  
  **Esperado**: HTTP 200, JSON con array `transferencias`

### Endpoint: GET /api/cuentas/{numero}

- [ ] Consulta de cuenta funciona
  ```powershell
  Invoke-WebRequest -Uri "http://localhost:8000/api/cuentas/12345678" -UseBasicParsing | ConvertFrom-Json
  ```
  
  **Esperado**: HTTP 200, JSON con `saldo`, `estado`, etc.

### Endpoint: POST /api/cuentas/{numero}/reset

- [ ] Reset de cuenta funciona
  ```powershell
  Invoke-WebRequest -Uri "http://localhost:8000/api/cuentas/12345678/reset" -Method POST -UseBasicParsing | ConvertFrom-Json
  ```
  
  **Esperado**: HTTP 200, saldo reseteado a 100,000

---

## 📦 Postman - Verificación

- [ ] Archivo JSON existe
  ```powershell
  Test-Path "Transferencias_Bancarias.postman_collection.json"
  ```
  
  **Esperado**: True

- [ ] Archivo JSON es válido
  ```powershell
  Get-Content "Transferencias_Bancarias.postman_collection.json" | ConvertFrom-Json
  ```
  
  **Esperado**: No hay errores de parsing

- [ ] Colección importable en Postman
  1. Abrir Postman
  2. Import → File → Seleccionar archivo
  3. Verificar que aparece "Transferencias Bancarias - Test Suite"
  
  **Esperado**: Colección con 14+ requests

- [ ] Variables de colección configuradas
  En Postman, verificar variables:
  - `base_url`: http://localhost:8000
  - `auth_token`: Bearer test_token_123
  - `cuenta_origen`: 12345678
  - `cuenta_destino`: 87654321
  
  **Esperado**: Todas las variables definidas

---

## 📚 Documentación - Verificación

- [ ] README.md existe y es legible
  ```powershell
  Get-Content README.md | Select-Object -First 10
  ```

- [ ] DOCUMENTACION_TECNICA.md existe
  ```powershell
  Test-Path "DOCUMENTACION_TECNICA.md"
  ```

- [ ] COMANDOS_UTILES.md existe
  ```powershell
  Test-Path "COMANDOS_UTILES.md"
  ```

- [ ] RESUMEN_EJECUTIVO.md existe
  ```powershell
  Test-Path "RESUMEN_EJECUTIVO.md"
  ```

- [ ] INDICE.md existe
  ```powershell
  Test-Path "INDICE.md"
  ```

---

## 🎯 Validaciones de Negocio

### Límite Diario ($50,000)

- [ ] Reset cuenta antes de validar
  ```powershell
  curl -X POST http://localhost:8000/api/cuentas/12345678/reset
  ```

- [ ] Primera transferencia $30,000 pasa
  ```powershell
  $body = @{origen="12345678";destino="87654321";monto=30000} | ConvertTo-Json
  Invoke-WebRequest -Uri "http://localhost:8000/api/transferencias" -Method POST -Body $body -Headers @{"Content-Type"="application/json";"Authorization"="Bearer test"} -UseBasicParsing
  ```
  **Esperado**: HTTP 200

- [ ] Segunda transferencia $30,000 falla (total $60K > $50K)
  ```powershell
  $body = @{origen="12345678";destino="87654321";monto=30000} | ConvertTo-Json
  Invoke-WebRequest -Uri "http://localhost:8000/api/transferencias" -Method POST -Body $body -Headers @{"Content-Type"="application/json";"Authorization"="Bearer test"} -UseBasicParsing
  ```
  **Esperado**: HTTP 403, mensaje límite diario

### OTP para Montos > $1,000,000

- [ ] Reset cuenta
  ```powershell
  curl -X POST http://localhost:8000/api/cuentas/12345678/reset
  ```

- [ ] Transferencia $2M sin OTP falla
  ```powershell
  $body = @{origen="12345678";destino="87654321";monto=2000000} | ConvertTo-Json
  Invoke-WebRequest -Uri "http://localhost:8000/api/transferencias" -Method POST -Body $body -Headers @{"Content-Type"="application/json";"Authorization"="Bearer test"} -UseBasicParsing
  ```
  **Esperado**: HTTP 401, mensaje OTP requerido

- [ ] Transferencia $2M con OTP válido pasa
  ```powershell
  $body = @{origen="12345678";destino="87654321";monto=2000000;otp="123456"} | ConvertTo-Json
  Invoke-WebRequest -Uri "http://localhost:8000/api/transferencias" -Method POST -Body $body -Headers @{"Content-Type"="application/json";"Authorization"="Bearer test";"X-OTP"="123456"} -UseBasicParsing
  ```
  **Esperado**: HTTP 200 (si saldo y límites lo permiten)

### Concurrencia y Atomicidad

- [ ] Reset cuenta a $100,000
  ```powershell
  curl -X POST http://localhost:8000/api/cuentas/12345678/reset
  ```

- [ ] Dos transferencias simultáneas de $30K c/u
  - Una debe pasar (HTTP 200)
  - Otra debe fallar (HTTP 403) por límite diario
  
  **Esperado**: Solo una completa, la otra rechazada

---

## 🔐 Seguridad - Verificación

- [ ] Sin token rechaza (401)
- [ ] Token inválido rechaza (401)
- [ ] OTP inválido para montos altos rechaza (401)
- [ ] Rate limiting funciona (429 después de 10 requests)
- [ ] Cuenta bloqueada rechaza (403)

---

## 📈 Performance - Verificación

- [ ] Health check responde en < 100ms
- [ ] Transferencia simple responde en < 500ms
- [ ] Suite de 15 tests completa en < 120s

---

## 🧹 Limpieza - Opcional

Después de verificar todo:

- [ ] Detener API
  ```powershell
  Get-Process python | Stop-Process -Force
  ```

- [ ] Limpiar archivos generados (opcional)
  ```powershell
  Remove-Item -Force report.html, .coverage
  Remove-Item -Recurse -Force htmlcov, .pytest_cache
  ```

---

## ✅ Resultado Final

### Estado del Proyecto

- [ ] **Todos los checks anteriores pasaron**

### Checklist Resumen

- [ ] ✅ Instalación completa
- [ ] ✅ API funcional
- [ ] ✅ Tests ejecutándose (13/15 PASSED)
- [ ] ✅ Reportes generándose
- [ ] ✅ Endpoints validados
- [ ] ✅ Postman importable
- [ ] ✅ Documentación completa
- [ ] ✅ Validaciones de negocio funcionando
- [ ] ✅ Seguridad implementada

---

## 🎉 ¡Proyecto Validado!

Si todos los checks pasaron, el proyecto está **100% funcional** y listo para:
- ✅ Ejercicios prácticos de QA
- ✅ Demostraciones
- ✅ Capacitación
- ✅ Base para proyectos reales

---

**Fecha de verificación**: _____________  
**Verificado por**: _____________  
**Resultado**: ✅ APROBADO / ❌ REQUIERE AJUSTES

---

## 📞 Si algo falla...

1. **Revisar logs en consola** donde corre la API
2. **Consultar** [DOCUMENTACION_TECNICA.md](./DOCUMENTACION_TECNICA.md) → Troubleshooting
3. **Verificar** que puerto 8000 esté libre: `netstat -ano | findstr :8000`
4. **Reiniciar** API: detener proceso y ejecutar `python main.py` nuevamente
5. **Reset cuenta** antes de tests: `curl -X POST http://localhost:8000/api/cuentas/12345678/reset`

---

**Última actualización**: 2025-12-10  
**Versión**: 1.0.0
