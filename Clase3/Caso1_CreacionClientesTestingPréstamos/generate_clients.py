import random
import json
from datetime import datetime

random.seed(42)
NUM = 1000
OUT_FILE = "c:\\Users\\1577089\\Desktop\\CapacitacionIA-Banistmo\\CapacitacionIA-Banistmo\\Clase3\\Caso1_CreacionClientesTestingPréstamos\\clientes_test_1000.json"
DATE_STR = datetime.now().strftime("%Y%m%d")

first_names = [
    "Sof\u00eda","Valentina","Isabella","Mariana","Laura","Camila","Daniela","Andrea","Natalia","Lucia",
    "Juan","Santiago","Mateo","Sebasti\u00e1n","Alejandro","Daniel","David","Carlos","Juan Pablo","Andr\u00e9s",
    "Javier","Luis","Pedro","Miguel","Roberto","Fernando","Diego","Nicol\u00e1s","Marcos","Ricardo",
]
last_names = [
    "Gonz\u00e1lez","Rodr\u00edguez","Mart\u00ednez","Garc\u00eda","L\u00f3pez","Hern\u00e1ndez","P\u00e9rez","S\u00e1nchez","Romero","Torres",
    "Ram\u00edrez","Flores","Rojas","Guti\u00e9rrez","D\u00edaz","Vargas","Castro","Ortiz","Ruiz","Mendoza",
]

other_cities = ["Bucaramanga","Barranquilla","Pereira","Manizales","Cartagena","Ibagu\u00e9","Tunja","Sincelejo","Monter\u00eda","Neiva"]

domains = ["empresa.com","financiera.com","banco.com","corp.com"]

# Precompute distributions as lists to guarantee exact counts
profiles = (['Excelente'] * 200) + (['Bueno'] * 400) + (['Regular'] * 300) + (['Malo'] * 100)
random.shuffle(profiles)

cities = (['Bogot\u00e1'] * 400) + (['Medell\u00edn'] * 200) + (['Cali'] * 150)
# others 250
for _ in range(250):
    cities.append(random.choice(other_cities))
random.shuffle(cities)

emp_types = (['Empleado'] * 700) + (['Independiente'] * 200) + (['Pensionado'] * 100)
random.shuffle(emp_types)

# Generate unique cedulas (10 digits) and unique emails
cedula_base = 1000000000
cedulas = list(range(cedula_base, cedula_base + NUM))
random.shuffle(cedulas)

# helper to create full name

def make_name():
    fn = random.choice(first_names)
    ln1 = random.choice(last_names)
    ln2 = random.choice(last_names)
    # avoid same surname twice
    while ln2 == ln1:
        ln2 = random.choice(last_names)
    return f"{fn} {ln1} {ln2}", fn, ln1

clients = []
used_emails = set()

for i in range(NUM):
    profile = profiles[i]
    city = cities[i]
    emp = emp_types[i]

    # Birth year: if pensionado prefer older (>=55)
    if emp == 'Pensionado':
        birth_year = random.randint(1960, 1970)
    else:
        birth_year = random.randint(1960, 2000)
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)
    fechaNacimiento = f"{birth_year:04d}-{birth_month:02d}-{birth_day:02d}"
    age = datetime.now().year - birth_year

    # ingreso mensual
    ingresoMensual = random.randint(1500000, 20000000)

    # deudaActual based on profile
    if profile == 'Excelente':
        deuda_pct = random.uniform(0.0, 0.19)
        score = random.randint(750, 850)
        historial = 'Excelente'
    elif profile == 'Bueno':
        deuda_pct = random.uniform(0.20, 0.39)
        score = random.randint(650, 749)
        historial = 'Bueno'
    elif profile == 'Regular':
        deuda_pct = random.uniform(0.40, 0.59)
        score = random.randint(550, 649)
        historial = 'Regular'
    else:
        deuda_pct = random.uniform(0.60, 0.80)
        score = random.randint(300, 549)
        historial = 'Malo'

    deudaActual = int(min(int(deuda_pct * ingresoMensual), int(0.8 * ingresoMensual)))

    saldoCuentaAhorros = random.randint(0, 50000000)

    # antiguedad laboral consistent with age: maxYears = min(30, age-18)
    max_years = max(0, min(30, age - 18))
    antiguedadLaboral = random.randint(0, max_years) if max_years > 0 else 0

    nombreCompleto, first, last = make_name()

    # phone +57 3XX XXX XXXX
    prefix = random.choice(['300','301','302','303','304','305','310','311','312','313','314','315','320','321','322','323','350','351','352','353','355'])
    part1 = random.randint(100, 999)
    part2 = random.randint(1000, 9999)
    telefono = f"+57 {prefix} {part1:03d} {part2:04d}"

    cedula = str(cedulas[i])

    # email unique: firstname.lastnameNN@domain
    base_email = f"{first}.{last}".lower().replace(' ', '')
    domain = random.choice(domains)
    email = f"{base_email}{i}@{domain}"
    # ensure unique
    if email in used_emails:
        email = f"{base_email}{i}-{random.randint(10,99)}@{domain}"
    used_emails.add(email)

    # id
    id_seq = i+1
    id_str = f"CLT-{DATE_STR}-{id_seq:04d}"

    cliente = {
        "id": id_str,
        "cedulaCiudadania": cedula,
        "nombreCompleto": nombreCompleto,
        "email": email,
        "telefono": telefono,
        "fechaNacimiento": fechaNacimiento,
        "ciudadResidencia": city,
        "ingresoMensual": ingresoMensual,
        "tipoEmpleo": emp,
        "antiguedadLaboral": antiguedadLaboral,
        "historialCrediticio": historial,
        "deudaActual": deudaActual,
        "saldoCuentaAhorros": saldoCuentaAhorros,
        "scoreCrediticio": score
    }

    clients.append(cliente)

# Final validations (simple asserts)
assert len(set(c['cedulaCiudadania'] for c in clients)) == NUM
assert len(set(c['email'] for c in clients)) == NUM

# write file
with open(OUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(clients, f, ensure_ascii=False, indent=2)

print(f"Generados {NUM} clientes en: {OUT_FILE}")
