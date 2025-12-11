import json
import csv
import re
from pathlib import Path

BASE = Path(r"c:\Users\1577089\Desktop\CapacitacionIA-Banistmo\CapacitacionIA-Banistmo\Clase3\Caso1_CreacionClientesTestingPréstamos")
CLIENTS_JSON = BASE / 'clientes_test_1000.json'
REPORT_JSON = BASE / 'tests' / 'test_report.json'
REPORT_TXT = BASE / 'tests' / 'test_report.txt'

OUT_CLIENTS_CSV = BASE / 'clientes_test_1000.csv'
OUT_SCENARIOS_CSV = BASE / 'escenarios_tests.csv'

# 1) Export clients JSON -> CSV
with open(CLIENTS_JSON, encoding='utf-8') as f:
    clients = json.load(f)

# Determine header order (fixed)
headers = [
    'id','cedulaCiudadania','nombreCompleto','email','telefono','fechaNacimiento',
    'ciudadResidencia','ingresoMensual','tipoEmpleo','antiguedadLaboral','historialCrediticio',
    'deudaActual','saldoCuentaAhorros','scoreCrediticio'
]

with open(OUT_CLIENTS_CSV, 'w', encoding='utf-8', newline='') as csvf:
    writer = csv.DictWriter(csvf, fieldnames=headers)
    writer.writeheader()
    for c in clients:
        # ensure all fields present
        row = {k: c.get(k, '') for k in headers}
        writer.writerow(row)

# 2) Export test scenarios -> CSV
# We'll read the TXT report and the JSON report timestamp
timestamp = ''
if REPORT_JSON.exists():
    with open(REPORT_JSON, encoding='utf-8') as rj:
        jr = json.load(rj)
        timestamp = jr.get('timestamp','')

text = ''
if REPORT_TXT.exists():
    with open(REPORT_TXT, encoding='utf-8') as rt:
        text = rt.read()

# parse lines like: test_name (module.ClassName.method) ... ok
pattern = re.compile(r'^(?P<name>[^\s]+) \((?P<class>[^)]+)\) \.\.\. (?P<status>ok|FAIL|ERROR|skipped)$', re.MULTILINE)
scenarios = []
for m in pattern.finditer(text):
    name = m.group('name')
    fullclass = m.group('class')
    status = m.group('status')
    scenarios.append({'test_name': name, 'classname': fullclass, 'status': status, 'message':'', 'timestamp': timestamp})

# If no scenarios found, fallback to reading test_report.json counts
if not scenarios and REPORT_JSON.exists():
    # create placeholder rows from json summary
    with open(REPORT_JSON, encoding='utf-8') as rj:
        jr = json.load(rj)
    scenarios.append({'test_name':'summary','classname':'unittest','status':'OK' if jr.get('wasSuccessful') else 'FAIL','message':'summary','timestamp':jr.get('timestamp','')})

with open(OUT_SCENARIOS_CSV, 'w', encoding='utf-8', newline='') as scsv:
    fieldnames = ['test_name','classname','status','message','timestamp']
    writer = csv.DictWriter(scsv, fieldnames=fieldnames)
    writer.writeheader()
    for s in scenarios:
        writer.writerow(s)

print('CSV generados:')
print(OUT_CLIENTS_CSV)
print(OUT_SCENARIOS_CSV)
