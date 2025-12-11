import json
from collections import Counter
f = r"c:\Users\1577089\Desktop\CapacitacionIA-Banistmo\CapacitacionIA-Banistmo\Clase3\Caso1_CreacionClientesTestingPréstamos\clientes_test_1000.json"
with open(f, encoding='utf-8') as fh:
    d = json.load(fh)

print('Total registros:', len(d))
print('Historial crediticio:', Counter(x['historialCrediticio'] for x in d))
print('Tipo empleo:', Counter(x['tipoEmpleo'] for x in d))
# city distribution (top counts)
cityc = Counter(x['ciudadResidencia'] for x in d)
print('Ciudades top:', cityc.most_common(8))
print('Score range:', min(x['scoreCrediticio'] for x in d), max(x['scoreCrediticio'] for x in d))
# debt percentage by profile
for p in ['Excelente','Bueno','Regular','Malo']:
    items = [x for x in d if x['historialCrediticio']==p]
    if not items:
        continue
    avg_debt_pct = sum(x['deudaActual']/x['ingresoMensual'] for x in items)/len(items)
    print(p, 'count', len(items), 'avg deuda %', round(avg_debt_pct*100,2))

# quick validations
emails_unique = len(set(x['email'] for x in d)) == len(d)
ced_unique = len(set(x['cedulaCiudadania'] for x in d)) == len(d)
print('Emails únicos:', emails_unique, 'Cedulas únicas:', ced_unique)

# Scoring consistency check: ensure all scores fall in expected ranges for their historial
ok = True
for x in d:
    s = x['scoreCrediticio']
    h = x['historialCrediticio']
    if h=='Excelente' and not (750 <= s <= 850): ok = False
    if h=='Bueno' and not (650 <= s <= 749): ok = False
    if h=='Regular' and not (550 <= s <= 649): ok = False
    if h=='Malo' and not (300 <= s <= 549): ok = False
print('Scores consistentes con historial:', ok)
