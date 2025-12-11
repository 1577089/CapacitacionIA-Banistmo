# 📊 DOCUMENTACIÓN: Reportes SVE (Standard Verification Environment)

## ¿Qué es SVE?

**SVE (Standard Verification Environment)** es un formato estándar utilizado en la industria bancaria y financiera para documentar resultados de pruebas de software. Este formato permite:

- ✅ Trazabilidad completa de casos de prueba
- ✅ Integración con sistemas de gestión de calidad
- ✅ Auditoría y cumplimiento normativo
- ✅ Reportes ejecutivos y técnicos
- ✅ Análisis de tendencias de calidad

---

## 🎯 Características de los Reportes SVE Generados

### Formatos Disponibles

1. **XML** (`sve_report.xml`)
   - Formato estándar de intercambio
   - Compatible con herramientas de QA empresariales
   - Estructura jerárquica clara
   - Validable con esquemas XSD

2. **JSON** (`sve_report.json`)
   - Ideal para APIs y automatización
   - Fácil integración con dashboards
   - Compatible con herramientas modernas de análisis

3. **CSV** (`sve_report.csv`)
   - Abre directamente en Excel
   - Análisis rápido con tablas dinámicas
   - Fácil de compartir con stakeholders

---

## 📋 Estructura del Reporte SVE

### 1. Metadata (Metadatos)
Información general del proyecto y ejecución:

```json
{
  "metadata": {
    "project": "API Transferencias Bancarias - Testing QA",
    "generated_at": "2025-12-10T12:32:07.206286",
    "test_framework": "pytest",
    "environment": "Development"
  }
}
```

### 2. Summary (Resumen Ejecutivo)
Métricas agregadas de la ejecución:

```json
{
  "summary": {
    "total_tests": 15,
    "passed": 13,
    "failed": 0,
    "skipped": 2,
    "errors": 0,
    "pass_rate": "86.67%",
    "total_duration": "77.49s"
  }
}
```

### 3. Test Cases (Casos de Prueba Detallados)
Información completa de cada test:

```json
{
  "test_id": "TC-01",
  "test_name": "test_01_transferencia_exitosa",
  "status": "PASS",
  "duration": 4.093,
  "scenario": "Transferencia exitosa con datos válidos",
  "expected_result": "HTTP 200, estado COMPLETED",
  "actual_result": "Test ejecutado exitosamente según lo esperado",
  "error_message": "",
  "preconditions": "Cuentas válidas, saldo suficiente",
  "test_data": {...},
  "timestamp": "2025-12-10T12:30:53.620260"
}
```

---

## 🚀 Cómo Generar Reportes SVE

### Método 1: Usar el Script PowerShell (Recomendado)

```powershell
.\run_tests_sve.ps1
```

Este script:
1. ✅ Configura el entorno automáticamente
2. ✅ Limpia reportes anteriores
3. ✅ Ejecuta todos los tests
4. ✅ Genera los 3 formatos SVE (XML, JSON, CSV)
5. ✅ Muestra resumen de resultados

### Método 2: Ejecutar pytest Directamente

```powershell
$env:AUTH_TOKEN="Bearer test"
pytest -v
```

Los reportes SVE se generan automáticamente gracias al hook configurado en `conftest.py`.

---

## 📖 Cómo Leer los Reportes

### Formato XML

```xml
<TestCase id="TC-01" status="PASS">
  <Name>test_01_transferencia_exitosa_path_feliz</Name>
  <Scenario>Transferencia exitosa con datos válidos</Scenario>
  <Preconditions>Cuentas válidas, saldo suficiente, token válido</Preconditions>
  <ExpectedResult>HTTP 200, estado COMPLETED, saldo actualizado</ExpectedResult>
  <ActualResult>Test ejecutado exitosamente según lo esperado</ActualResult>
  <Duration>4.093s</Duration>
  <Timestamp>2025-12-10T12:30:53.620260</Timestamp>
</TestCase>
```

**Abrir con:**
```powershell
notepad sve_report.xml
# o
code sve_report.xml  # Visual Studio Code
```

### Formato JSON

```json
{
  "test_id": "TC-01",
  "test_name": "test_01_transferencia_exitosa_path_feliz",
  "status": "PASS",
  "duration": 4.093,
  "scenario": "Transferencia exitosa con datos válidos",
  "expected_result": "HTTP 200, estado COMPLETED, saldo actualizado",
  "actual_result": "Test ejecutado exitosamente según lo esperado"
}
```

**Abrir con:**
```powershell
code sve_report.json
# o para parsear en PowerShell:
Get-Content sve_report.json | ConvertFrom-Json
```

### Formato CSV

```csv
Test ID,Test Name,Status,Duration (s),Scenario,Expected Result,Actual Result
TC-01,test_01_transferencia_exitosa,PASS,4.093,Transferencia exitosa,...
```

**Abrir con:**
```powershell
start sve_report.csv  # Abre en Excel
```

---

## 🔍 Casos de Uso Prácticos

### 1. Análisis Rápido en Excel
```powershell
start sve_report.csv
```
Luego en Excel:
- Crear tabla dinámica
- Filtrar por Status (PASS/FAIL/SKIP)
- Calcular promedios de duración
- Generar gráficos de distribución

### 2. Integración con CI/CD
```powershell
# En pipeline de Azure DevOps o Jenkins
pytest -v
# Publicar sve_report.xml como artefacto
# Parsear sve_report.json para métricas
```

### 3. Dashboard de Calidad
```javascript
// Consumir JSON desde aplicación web
fetch('sve_report.json')
  .then(r => r.json())
  .then(data => {
    console.log(`Pass Rate: ${data.summary.pass_rate}`);
    console.log(`Total Tests: ${data.summary.total_tests}`);
  });
```

### 4. Auditoría y Trazabilidad
```powershell
# Buscar test específico en XML
Select-String -Path "sve_report.xml" -Pattern "TC-08"

# Ver solo tests fallidos en JSON
$report = Get-Content sve_report.json | ConvertFrom-Json
$report.test_cases | Where-Object { $_.status -eq "FAIL" }
```

---

## 📊 Estados de Test Cases

| Estado | Descripción | Color Sugerido |
|--------|-------------|----------------|
| **PASS** | Test ejecutado exitosamente | 🟢 Verde |
| **FAIL** | Test falló (error en funcionalidad) | 🔴 Rojo |
| **SKIP** | Test omitido (condiciones no cumplidas) | 🟡 Amarillo |
| **ERROR** | Error de infraestructura/setup | 🟠 Naranja |

---

## 🔧 Personalización de Metadatos

Los metadatos de cada test se definen en `tests/conftest.py`:

```python
TEST_METADATA = {
    "test_01_transferencia_exitosa": {
        "id": "TC-01",
        "scenario": "Transferencia exitosa con datos válidos",
        "expected": "HTTP 200, estado COMPLETED",
        "preconditions": "Cuentas válidas, saldo suficiente"
    },
    # ... más tests
}
```

Para agregar un nuevo test al reporte SVE:
1. Agregar entrada en `TEST_METADATA`
2. Definir `id`, `scenario`, `expected`, `preconditions`
3. Ejecutar tests normalmente

---

## 📈 Métricas Incluidas en el Reporte

### Métricas de Ejecución
- ✅ **Total Tests**: Cantidad total de casos de prueba
- ✅ **Passed**: Tests exitosos
- ✅ **Failed**: Tests fallidos
- ✅ **Skipped**: Tests omitidos
- ✅ **Errors**: Errores de infraestructura
- ✅ **Pass Rate**: Porcentaje de éxito (Passed / Total)
- ✅ **Total Duration**: Tiempo total de ejecución

### Métricas por Test Case
- ✅ **Duration**: Tiempo de ejecución individual
- ✅ **Timestamp**: Momento exacto de ejecución
- ✅ **Status**: Estado final del test
- ✅ **Error Message**: Detalles de errores (si aplica)
- ✅ **Test Data**: Datos utilizados en el test

---

## 🎯 Ejemplo de Análisis de Resultados

### Análisis de Duración de Tests

```powershell
# PowerShell: Encontrar tests más lentos
$report = Get-Content sve_report.json | ConvertFrom-Json
$report.test_cases | 
    Sort-Object -Property duration -Descending | 
    Select-Object -First 5 test_name, duration
```

### Tasa de Éxito por Categoría

```powershell
# Ver distribución de estados
$report = Get-Content sve_report.json | ConvertFrom-Json
$report.test_cases | 
    Group-Object status | 
    Select-Object Name, Count
```

---

## 🔗 Integración con Herramientas Empresariales

### Jenkins
```groovy
// Publicar resultados SVE
publishHTML([
    reportDir: '.',
    reportFiles: 'sve_report.xml',
    reportName: 'SVE Test Report'
])
```

### Azure DevOps
```yaml
# azure-pipelines.yml
- task: PublishTestResults@2
  inputs:
    testResultsFormat: 'JUnit'
    testResultsFiles: 'sve_report.xml'
```

### Jira / TestRail
- Importar `sve_report.csv` directamente
- Mapear columnas: Test ID → Case ID
- Actualizar resultados automáticamente

---

## 📁 Archivos del Sistema SVE

```
Ejemplo2_TransferenciaBancaria/
├── tests/
│   ├── sve_reporter.py         # Motor de generación SVE
│   ├── conftest.py             # Configuración pytest + SVE
│   └── test_transferencias.py  # Tests con metadatos
├── run_tests_sve.ps1           # Script automatizado
├── sve_report.xml              # Reporte XML ✅
├── sve_report.json             # Reporte JSON ✅
└── sve_report.csv              # Reporte CSV ✅
```

---

## 🎓 Beneficios del Formato SVE

### Para QA
- ✅ Trazabilidad completa de cada test
- ✅ Evidencia para auditorías
- ✅ Fácil identificación de regresiones

### Para Developers
- ✅ Detalles técnicos de fallos
- ✅ Duración de tests para optimización
- ✅ Integración con CI/CD

### Para Managers
- ✅ Pass Rate visible al instante
- ✅ Reportes ejecutivos en Excel
- ✅ Métricas de calidad objetivas

### Para Auditoría
- ✅ Formato estándar reconocido
- ✅ Timestamps de ejecución
- ✅ Datos de prueba documentados

---

## 🚨 Troubleshooting

### Problema: No se generan reportes SVE
**Solución:**
```powershell
# Verificar que conftest.py esté en tests/
ls tests/conftest.py

# Verificar imports de pytest
python -c "import pytest; print(pytest.__version__)"
```

### Problema: Reportes vacíos
**Solución:**
```powershell
# Ejecutar con verbose para ver hooks
pytest -v --debug
```

### Problema: Encoding incorrecto en CSV
**Solución:**
```powershell
# Abrir CSV con encoding UTF-8
Get-Content sve_report.csv -Encoding UTF8
```

---

## 📚 Referencias y Estándares

- **IEEE 829**: Standard for Software Test Documentation
- **ISO/IEC 29119**: Software Testing Standards
- **SVE Framework**: Banking Industry Best Practices

---

## 🎉 Resumen

Los reportes SVE proveen:
1. ✅ **3 formatos** (XML, JSON, CSV)
2. ✅ **Generación automática** con cada ejecución de pytest
3. ✅ **Metadatos completos** de cada test case
4. ✅ **Métricas ejecutivas** (pass rate, duración, etc.)
5. ✅ **Trazabilidad** completa para auditorías
6. ✅ **Integración fácil** con herramientas empresariales

---

**Para generar reportes ahora:**
```powershell
.\run_tests_sve.ps1
```

**Archivos generados:**
- `sve_report.xml` - Formato XML estándar
- `sve_report.json` - Formato JSON para APIs
- `sve_report.csv` - Formato CSV para Excel

---

**Documentación completa**: Este archivo  
**Código fuente**: `tests/sve_reporter.py`  
**Configuración**: `tests/conftest.py`  
**Script automatizado**: `run_tests_sve.ps1`
