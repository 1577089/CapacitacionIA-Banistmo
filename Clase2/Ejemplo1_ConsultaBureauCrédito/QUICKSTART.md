# 🚀 Quick Start - Suite de Pruebas Bureau de Crédito

## Instalación Rápida (3 minutos)

### 1️⃣ Preparar Entorno
```powershell
# Navegar al directorio
cd C:\Users\1577089\Desktop\CapacitacionIA-Banistmo\CapacitacionIA-Banistmo

# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2️⃣ Configurar Variables
```powershell
# Copiar archivo de configuración
cp .env.example .env

# El archivo ya tiene valores por defecto para localhost:8000
# API_BASE_URL=http://localhost:8000
# API_TIMEOUT=5
```

### 3️⃣ Verificar API Activo
```powershell
# Asegúrate que tu API esté corriendo en localhost:8000
# Verificar con: http://localhost:8000/docs
```

### 4️⃣ Ejecutar Pruebas
```powershell
# Ejecutar todas las pruebas
pytest

# Solo pruebas críticas (recomendado para primera ejecución)
pytest -m critical -v
```

---

## 📊 Comandos Más Útiles

```powershell
# Ver todas las pruebas sin ejecutar
pytest --collect-only

# Ejecutar con reporte detallado
pytest -v

# Solo pruebas críticas (P0) - 4 tests
pytest -m critical

# Críticas + Alta prioridad (P0 + P1) - 11 tests
pytest -m "critical or high"

# Suite de regresión completa
pytest -m regression

# Un test específico
pytest tests/test_bureau_happy_path.py::TestBureauHappyPath::test_tc_bc_001_cliente_buen_historial -v

# Detener en primer error
pytest -x

# Mostrar prints
pytest -s

# Generar reporte HTML
pytest --html=report.html --self-contained-html
```

---

## 📁 Estructura del Proyecto

```
CapacitacionIA-Banistmo/
├── tests/
│   ├── conftest.py                     # ⚙️ Configuración pytest
│   ├── test_bureau_happy_path.py       # ✅ TC-BC-001 a 004 (P0)
│   ├── test_bureau_validations.py     # 🔍 TC-BC-005 a 007 (P1)
│   ├── test_bureau_errors.py          # ⚠️ TC-BC-008, 009, 015 (P0-P1)
│   ├── test_bureau_edge_cases.py      # 🎯 TC-BC-010 a 014 (P1-P2)
│   ├── test_data/
│   │   └── bureau_test_data.py         # 📊 Datos de prueba
│   └── helpers/
│       └── api_client.py               # 🔌 Cliente HTTP
├── requirements.txt                    # 📦 Dependencias
├── pytest.ini                          # ⚙️ Configuración pytest
├── .env.example                        # 🔐 Template variables
├── README.md                           # 📖 Documentación principal
├── MANUAL_PRUEBAS.md                   # 📚 Manual detallado
└── run_tests.py                        # 🎬 Script de ejecución
```

---

## ✅ Checklist Pre-Ejecución

- [ ] API corriendo en `localhost:8000`
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Archivo `.env` configurado
- [ ] Python 3.8+ instalado

---

## 🎯 Cobertura de Tests (15 casos)

### Prioridad P0 - Crítica (4 tests) ⭐
- ✅ TC-BC-001: Cliente con buen historial
- ✅ TC-BC-002: Cliente con deudas activas
- ✅ TC-BC-003: Cliente con mora
- ✅ TC-BC-004: Cliente en CIFIN

### Prioridad P1 - Alta (7 tests)
- ✅ TC-BC-005: Documento inválido
- ✅ TC-BC-006: Longitud incorrecta
- ✅ TC-BC-007: Tipo documento inválido
- ✅ TC-BC-009: Respuesta inválida
- ✅ TC-BC-010: Cliente extranjero
- ✅ TC-BC-011: Sin historial
- ✅ TC-BC-014: Score límite 600
- ✅ TC-BC-015: Campo null

### Prioridad P2 - Media (2 tests)
- ✅ TC-BC-012: Consulta duplicada
- ✅ TC-BC-013: Consulta histórica

### Casos de Timeout
- ✅ TC-BC-008: Timeout 5 segundos

---

## 🔥 Primera Ejecución Recomendada

```powershell
# 1. Verificar instalación
python --version
pip list | Select-String "pytest"

# 2. Verificar API
# Abrir navegador: http://localhost:8000/docs

# 3. Ejecutar smoke tests (solo críticos)
pytest -m critical -v

# 4. Si todo pasa, ejecutar suite completa
pytest -v
```

---

## 📊 Resultado Esperado

```
tests/test_bureau_happy_path.py::TestBureauHappyPath::test_tc_bc_001_cliente_buen_historial PASSED [7%]
tests/test_bureau_happy_path.py::TestBureauHappyPath::test_tc_bc_002_cliente_deudas_activas_al_dia PASSED [13%]
tests/test_bureau_happy_path.py::TestBureauHappyPath::test_tc_bc_003_cliente_con_mora_actual PASSED [20%]
tests/test_bureau_happy_path.py::TestBureauHappyPath::test_tc_bc_004_cliente_en_lista_cifin PASSED [27%]
...

========================== 15 passed in 3.45s ==========================
```

---

## ❓ Troubleshooting Rápido

### Error: "API no está disponible"
```powershell
# Verificar que el API esté corriendo
Test-NetConnection -ComputerName localhost -Port 8000
```

### Error: "ModuleNotFoundError: No module named 'pytest'"
```powershell
pip install -r requirements.txt
```

### Tests toman mucho tiempo
```powershell
# Ejecutar solo críticos
pytest -m critical
```

### Ver más detalles de un fallo
```powershell
pytest -vv --tb=long
```

---

## 📚 Más Información

- **Manual Detallado**: Ver `MANUAL_PRUEBAS.md`
- **README Completo**: Ver `README.md`
- **Documentación API**: http://localhost:8000/docs

---

## 🎓 Casos de Uso Comunes

### Para Desarrollo Diario
```powershell
# Antes de commit
pytest -m "critical or high" -x
```

### Para CI/CD
```powershell
# En pipeline de integración continua
pytest -m critical --junitxml=report.xml
```

### Para Release
```powershell
# Suite completa de regresión
pytest -m regression --html=report.html --self-contained-html
```

### Para Debugging
```powershell
# Un test específico con prints
pytest tests/test_bureau_happy_path.py::TestBureauHappyPath::test_tc_bc_001_cliente_buen_historial -s -vv
```

---

## 🚀 ¡Listo para Probar!

```powershell
pytest -m critical -v
```

**¡Éxito con las pruebas!** 🎉
