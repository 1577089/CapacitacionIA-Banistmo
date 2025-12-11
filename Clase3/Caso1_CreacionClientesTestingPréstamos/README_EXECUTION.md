# Caso1_CreacionClientesTestingPréstamos — Guía de configuración y ejecución

Este repositorio contiene un generador de datos sintéticos (1000 clientes), una suite de tests automatizados y scripts para generar reportes (JSON, TXT, HTML, JUnit XML) y exportar CSVs.

Rutas importantes (carpeta del caso):

- `generate_clients.py` — script que genera el dataset JSON: `clientes_test_1000.json`
- `clientes_test_1000.json` — dataset generado (array JSON con 1000 objetos)
- `clientes_test_1000.csv` — export CSV con los 1000 clientes (generado por `export_to_csv.py`)
- `tests/test_clients.py` — suite `unittest` que valida el dataset
- `run_tests_and_report.py` — ejecuta tests y genera reportes (JSON, TXT, HTML, JUnit XML)
- `export_to_csv.py` — genera `clientes_test_1000.csv` y `escenarios_tests.csv` a partir del JSON y reportes
- `run_tests.ps1` — runner PowerShell (Windows) para ejecutar tests y abrir `test_report.html`
- `run_tests.sh` — runner shell para Linux/WSL (abre `test_report.html` si existe)
- `tests/test_report.*` — reportes generados en la carpeta `tests` (`.json`, `.txt`, `.html`, `.junit.xml`)

Requisitos previos
------------------

- Python 3.8 o superior instalado y accesible desde la línea de comandos (`python`).
- En Windows, PowerShell (v5.1 o superior) para usar `run_tests.ps1`.
- En Unix/WSL, `bash` y un navegador/`xdg-open` para abrir HTML.

Instalación / Preparación
-------------------------

No hay dependencias externas obligatorias para ejecutar los scripts proporcionados. Opcionalmente puedes crear un entorno virtual:

PowerShell (Windows):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

Unix / WSL:

```bash
python -m venv .venv; source .venv/bin/activate
```

Ejecución paso a paso (Windows)
-------------------------------

1. Generar dataset (si aún no existe):

```powershell
cd 'c:\Users\1577089\Desktop\CapacitacionIA-Banistmo\CapacitacionIA-Banistmo\Clase3\Caso1_CreacionClientesTestingPréstamos'
python generate_clients.py
```

2. Ejecutar tests y generar reportes (JSON, TXT, HTML, JUnit XML):

```powershell
.\run_tests.ps1
# o directamente
python run_tests_and_report.py
```

3. Revisar reportes generados en `tests/`:

- `tests/test_report.json` — resumen de ejecución
- `tests/test_report.txt` — salida completa de la ejecución
- `tests/test_report.html` — reporte legible (se abre automáticamente con `run_tests.ps1`)
- `tests/test_report.junit.xml` — archivo JUnit XML para CI

4. Exportar CSVs (clientes y escenarios):

```powershell
python export_to_csv.py
# Salidas: clientes_test_1000.csv  y  escenarios_tests.csv
```

Ejecución paso a paso (Unix / WSL)
---------------------------------

```bash
cd "/ruta/al/proyecto/Clase3/Caso1_CreacionClientesTestingPréstamos"
python3 generate_clients.py
./run_tests.sh
python3 export_to_csv.py
```

Qué contienen los CSVs
----------------------

- `clientes_test_1000.csv`: columnas — `id, cedulaCiudadania, nombreCompleto, email, telefono, fechaNacimiento, ciudadResidencia, ingresoMensual, tipoEmpleo, antiguedadLaboral, historialCrediticio, deudaActual, saldoCuentaAhorros, scoreCrediticio`.
- `escenarios_tests.csv`: columnas — `test_name, classname, status, message, timestamp`.

Integración con CI
------------------

- Puedes subir `tests/test_report.junit.xml` como artifact de build en tu CI (GitHub Actions, GitLab CI, Azure pipelines) para visualizar resultados en la interfaz.
- Alternativa (recomendada): usar `pytest --junitxml=report.xml` o `unittest-xml-reporting` para trazas completas y mayor compatibilidad.

Notas y consideraciones
-----------------------

- Los datos generados son sintéticos y no corresponden a personas reales; está diseñados para testing de scoring.
- La generación actual produce distribuciones y validaciones conforme a la especificación del proyecto (perfiles: Excelente/Bueno/Regular/Malo; distribución por ciudad; rangos de ingreso y score).
- Si necesitas formatos distintos (Excel `.xlsx`, delimitador `;`, o ZIP con artefactos), puedo añadir un script que convierta o empaquete automáticamente.

Comandos útiles rápidos
-----------------------

PowerShell — ejecutar todo y abrir reporte:

```powershell
cd '...\Caso1_CreacionClientesTestingPréstamos'
.\run_tests.ps1
```

Unix/WSL — ejecutar todo y abrir reporte:

```bash
cd "/ruta/.../Caso1_CreacionClientesTestingPréstamos"
./run_tests.sh
```

Soporte
-------

Si quieres que adapte los scripts para:

- producir `clientes_test_1000.sv` con `;` como separador,
- exportar directamente a `.xlsx`,
- incluir trazas completas de fallos en `test_report.junit.xml`,

indícame cuál prefieres y lo implemento.
