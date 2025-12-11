# Dataset & Test Runner - Caso1_CreacionClientesTestingPréstamos

Contenido:
- `generate_clients.py` — script que genera `clientes_test_1000.json` (dataset sintético de 1000 clientes).
- `clientes_test_1000.json` — dataset generado.
- `tests/test_clients.py` — suite `unittest` que valida el dataset.
- `run_tests_and_report.py` — ejecuta los tests y genera reportes: JSON, TXT, HTML y JUnit XML.
- `run_tests.ps1` — script PowerShell para ejecutar y abrir el reporte HTML (Windows).
- `run_tests.sh` — script shell para entornos Unix (añadido).

Cómo ejecutar (Windows PowerShell):
```powershell
cd "c:\Users\1577089\Desktop\CapacitacionIA-Banistmo\CapacitacionIA-Banistmo\Clase3\Caso1_CreacionClientesTestingPréstamos"
.\run_tests.ps1
```

Cómo ejecutar (Unix / WSL):
```bash
cd "/path/to/Clase3/Caso1_CreacionClientesTestingPréstamos"
./run_tests.sh
```

Reportes generados por `run_tests_and_report.py`:
- `tests/test_report.json` — resumen en JSON
- `tests/test_report.txt` — salida legible
- `tests/test_report.html` — reporte HTML legible
- `tests/test_report.junit.xml` — JUnit XML (para CI)

Notas:
- `run_tests_and_report.py` intenta generar `test_report.junit.xml` analizando la salida del runner; si usas `pytest` o `xmlrunner` en CI, la integración JUnit será más completa.
- Si quieres que genere JUnit con trazas completas, puedo actualizar el runner para usar `xmlrunner` o `pytest --junitxml`.
