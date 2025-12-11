# Ejecutar todas las pruebas
pytest

# Ejecutar con reporte detallado
pytest -v

# Ejecutar solo pruebas críticas
pytest -m critical

# Ejecutar pruebas de alta prioridad
pytest -m high

# Ejecutar pruebas críticas y de alta prioridad
pytest -m "critical or high"

# Ejecutar suite de regresión
pytest -m regression

# Ejecutar pruebas de validación
pytest -m validation

# Ejecutar pruebas de edge cases
pytest -m edge_case

# Ejecutar archivo específico
pytest tests/test_bureau_happy_path.py

# Ejecutar test específico
pytest tests/test_bureau_happy_path.py::TestBureauHappyPath::test_tc_bc_001_cliente_buen_historial

# Ejecutar con reporte de cobertura
pytest --cov=tests --cov-report=html

# Ejecutar y detener en primer error
pytest -x

# Ejecutar tests en paralelo (requiere pytest-xdist)
pytest -n auto

# Generar reporte JUnit (para CI/CD)
pytest --junitxml=report.xml

# Mostrar print statements
pytest -s

# Modo verbose con traceback completo
pytest -vv --tb=long
