# Suite de Pruebas Automatizadas - Bureau de Crédito

## Descripción
Suite completa de pruebas automatizadas para el sistema de consulta de Bureau de Crédito, implementando 15 casos de prueba críticos para sistemas bancarios.

## Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt
```

## Configuración

```bash
# Copiar archivo de configuración
cp .env.example .env

# Editar variables de entorno según necesidad
```

## Ejecución de Pruebas

### Ejecutar todas las pruebas
```bash
pytest
```

### Ejecutar por prioridad
```bash
# Solo casos críticos (P0)
pytest -m critical

# Casos críticos y alta prioridad (P0 + P1)
pytest -m "critical or high"
```

### Ejecutar por tipo
```bash
# Pruebas de validación
pytest -m validation

# Pruebas de timeout
pytest -m timeout

# Edge cases
pytest -m edge_case
```

### Ejecutar suite específica
```bash
# Path feliz y casos positivos
pytest tests/test_bureau_happy_path.py

# Validaciones
pytest tests/test_bureau_validations.py

# Edge cases
pytest tests/test_bureau_edge_cases.py
```

### Generar reporte HTML
```bash
pytest --html=report.html --self-contained-html
```

## Estructura del Proyecto

```
tests/
├── conftest.py              # Configuración y fixtures
├── test_bureau_happy_path.py    # TC-BC-001 a TC-BC-004
├── test_bureau_validations.py  # TC-BC-005 a TC-BC-007
├── test_bureau_errors.py        # TC-BC-008, TC-BC-009, TC-BC-015
├── test_bureau_edge_cases.py   # TC-BC-010 a TC-BC-014
├── test_data/
│   └── bureau_test_data.py      # Datos de prueba
└── helpers/
    └── api_client.py            # Cliente HTTP helper
```

## Cobertura de Casos de Prueba

| ID | Escenario | Prioridad | Archivo |
|---|---|---|---|
| TC-BC-001 | Cliente con buen historial | P0 | test_bureau_happy_path.py |
| TC-BC-002 | Cliente con deudas activas | P0 | test_bureau_happy_path.py |
| TC-BC-003 | Cliente con mora actual | P0 | test_bureau_happy_path.py |
| TC-BC-004 | Cliente en CIFIN | P0 | test_bureau_happy_path.py |
| TC-BC-005 | Documento inválido | P1 | test_bureau_validations.py |
| TC-BC-006 | Longitud incorrecta | P1 | test_bureau_validations.py |
| TC-BC-007 | Tipo documento inválido | P1 | test_bureau_validations.py |
| TC-BC-008 | Timeout 5 segundos | P0 | test_bureau_errors.py |
| TC-BC-009 | Respuesta inválida | P1 | test_bureau_errors.py |
| TC-BC-010 | Cliente extranjero | P1 | test_bureau_edge_cases.py |
| TC-BC-011 | Sin historial | P1 | test_bureau_edge_cases.py |
| TC-BC-012 | Documento duplicado | P2 | test_bureau_edge_cases.py |
| TC-BC-013 | Consulta histórica | P2 | test_bureau_edge_cases.py |
| TC-BC-014 | Score límite 600 | P1 | test_bureau_edge_cases.py |
| TC-BC-015 | Campo null | P1 | test_bureau_errors.py |
