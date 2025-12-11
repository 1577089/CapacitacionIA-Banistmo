# ✅ VERIFICACIÓN DE INSTALACIÓN

Para verificar que todo está correctamente instalado, ejecuta estos comandos:

## 1. Verificar Python
```powershell
python --version
# Debe mostrar Python 3.8 o superior
```

## 2. Crear y activar entorno virtual (RECOMENDADO)
```powershell
cd C:\Users\1577089\Desktop\CapacitacionIA-Banistmo\CapacitacionIA-Banistmo
python -m venv venv
.\venv\Scripts\activate
```

## 3. Instalar dependencias
```powershell
pip install -r requirements.txt
```

## 4. Verificar instalación de pytest
```powershell
pytest --version
# Debe mostrar: pytest 7.4.3
```

## 5. Listar tests disponibles
```powershell
pytest --collect-only
# Debe mostrar 15+ tests
```

## 6. Verificar que el API está corriendo
```powershell
# Abrir navegador en:
http://localhost:8000/docs
```

## 7. Ejecutar pruebas críticas
```powershell
pytest -m critical -v
```

---

# 📊 TESTS DISPONIBLES

Después de instalar, deberías ver estos tests:

## test_bureau_happy_path.py (4 tests)
- test_tc_bc_001_cliente_buen_historial
- test_tc_bc_002_cliente_deudas_activas_al_dia
- test_tc_bc_003_cliente_con_mora_actual
- test_tc_bc_004_cliente_en_lista_cifin

## test_bureau_validations.py (6 tests)
- test_tc_bc_005_documento_invalido_caracteres_especiales
- test_tc_bc_006_documento_longitud_incorrecta
- test_tc_bc_007_tipo_documento_invalido
- test_tc_bc_005_documento_vacio
- test_tc_bc_006_documento_solo_espacios
- test_tc_bc_007_tipo_documento_vacio

## test_bureau_errors.py (5 tests)
- test_tc_bc_008_timeout_5_segundos
- test_tc_bc_009_respuesta_invalida_del_bureau
- test_tc_bc_015_campo_documento_null
- test_tc_bc_008_verificar_retry_logic
- test_tc_bc_009_manejo_campo_faltante_en_respuesta

## test_bureau_edge_cases.py (6 tests)
- test_tc_bc_010_cliente_extranjero_pasaporte
- test_tc_bc_011_cliente_sin_historial_crediticio
- test_tc_bc_012_documento_duplicado_consulta_simultanea
- test_tc_bc_013_consulta_historica_cache
- test_tc_bc_014_cliente_score_limite_600
- test_tc_bc_014_scores_frontera

**TOTAL: 21 tests** (algunos adicionales para mayor cobertura)

---

# 🚀 PRIMEROS PASOS

```powershell
# 1. Activar entorno (si lo creaste)
.\venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ver estructura de tests
pytest --collect-only -q

# 4. Ejecutar solo críticos (recomendado para primera vez)
pytest -m critical -v

# 5. Si todo pasa, ejecutar suite completa
pytest -v
```

---

# ❌ TROUBLESHOOTING

## Error: "pytest no se reconoce"
**Solución**: Instalar dependencias
```powershell
pip install -r requirements.txt
```

## Error: "API no está disponible"
**Solución**: Asegurar que el API esté corriendo
```powershell
# Verificar conexión
Test-NetConnection -ComputerName localhost -Port 8000
```

## Error: "ModuleNotFoundError"
**Solución**: Activar entorno virtual e instalar dependencias
```powershell
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

# ✅ CHECKLIST COMPLETO

- [ ] Python 3.8+ instalado
- [ ] Entorno virtual creado (opcional pero recomendado)
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Archivo `.env` configurado
- [ ] API corriendo en localhost:8000
- [ ] pytest funcionando (`pytest --version`)
- [ ] Tests listados correctamente (`pytest --collect-only`)

---

# 🎯 UNA VEZ VERIFICADO TODO

Ejecuta:
```powershell
pytest -m critical -v
```

Deberías ver algo como:
```
tests/test_bureau_happy_path.py::TestBureauHappyPath::test_tc_bc_001... PASSED
tests/test_bureau_happy_path.py::TestBureauHappyPath::test_tc_bc_002... PASSED
tests/test_bureau_happy_path.py::TestBureauHappyPath::test_tc_bc_003... PASSED
tests/test_bureau_happy_path.py::TestBureauHappyPath::test_tc_bc_004... PASSED

========================== 4 passed in 2.34s ==========================
```

**¡Éxito!** 🎉
