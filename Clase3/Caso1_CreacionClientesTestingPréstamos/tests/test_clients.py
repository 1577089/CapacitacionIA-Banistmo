import unittest
import json
import re
from datetime import datetime
from collections import Counter

DATA_FILE = r"c:\Users\1577089\Desktop\CapacitacionIA-Banistmo\CapacitacionIA-Banistmo\Clase3\Caso1_CreacionClientesTestingPréstamos\clientes_test_1000.json"

class TestClientsDataset(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(DATA_FILE, encoding='utf-8') as f:
            cls.data = json.load(f)

    def test_count_1000(self):
        self.assertEqual(len(self.data), 1000, "Debe haber exactamente 1000 registros")

    def test_unique_cedula_and_email(self):
        cedulas = [x['cedulaCiudadania'] for x in self.data]
        emails = [x['email'] for x in self.data]
        self.assertEqual(len(set(cedulas)), len(cedulas), "Cédulas deben ser únicas")
        self.assertEqual(len(set(emails)), len(emails), "Emails deben ser únicos")

    def test_cedula_format(self):
        for c in self.data:
            self.assertTrue(re.fullmatch(r"\d{10}", c['cedulaCiudadania']), f"Cédula inválida: {c['cedulaCiudadania']}")

    def test_id_format(self):
        for c in self.data:
            self.assertTrue(re.fullmatch(r"CLT-\d{8}-\d{4}", c['id']), f"ID inválido: {c['id']}")

    def test_telefono_format(self):
        for c in self.data:
            self.assertTrue(re.fullmatch(r"\+57 3\d{2} \d{3} \d{4}", c['telefono']), f"Teléfono inválido: {c['telefono']}")

    def test_fecha_nacimiento_range(self):
        for c in self.data:
            y = int(c['fechaNacimiento'].split('-')[0])
            self.assertTrue(1960 <= y <= 2000, f"Año de nacimiento fuera de rango: {y}")

    def test_ingreso_and_saldo_ranges(self):
        for c in self.data:
            self.assertTrue(1500000 <= c['ingresoMensual'] <= 20000000, "Ingreso fuera de rango")
            self.assertTrue(0 <= c['saldoCuentaAhorros'] <= 50000000, "Saldo en cuenta fuera de rango")

    def test_tipo_empleo_distribution(self):
        cnt = Counter(x['tipoEmpleo'] for x in self.data)
        self.assertEqual(cnt['Empleado'], 700)
        self.assertEqual(cnt['Independiente'], 200)
        self.assertEqual(cnt['Pensionado'], 100)

    def test_historial_distribution(self):
        cnt = Counter(x['historialCrediticio'] for x in self.data)
        self.assertEqual(cnt['Excelente'], 200)
        self.assertEqual(cnt['Bueno'], 400)
        self.assertEqual(cnt['Regular'], 300)
        self.assertEqual(cnt['Malo'], 100)

    def test_city_distribution(self):
        cnt = Counter(x['ciudadResidencia'] for x in self.data)
        self.assertEqual(cnt['Bogotá'], 400)
        self.assertEqual(cnt['Medellín'], 200)
        self.assertEqual(cnt['Cali'], 150)
        others = sum(v for k,v in cnt.items() if k not in ('Bogotá','Medellín','Cali'))
        self.assertEqual(others, 250)

    def test_score_ranges_per_historial(self):
        for x in self.data:
            s = x['scoreCrediticio']
            h = x['historialCrediticio']
            if h=='Excelente':
                self.assertTrue(750 <= s <= 850)
            elif h=='Bueno':
                self.assertTrue(650 <= s <= 749)
            elif h=='Regular':
                self.assertTrue(550 <= s <= 649)
            elif h=='Malo':
                self.assertTrue(300 <= s <= 549)
            else:
                self.fail(f"Historial desconocido: {h}")

    def test_debt_consistency(self):
        for x in self.data:
            ingreso = x['ingresoMensual']
            deuda = x['deudaActual']
            self.assertTrue(deuda <= int(0.8 * ingreso), "Deuda excede 80% del ingreso")
            pct = deuda / ingreso if ingreso>0 else 0
            h = x['historialCrediticio']
            if h=='Excelente':
                self.assertTrue(pct < 0.20, f"Deuda incompatible para Excelente: {pct}")
            elif h=='Bueno':
                self.assertTrue(0.20 <= pct < 0.40, f"Deuda incompatible para Bueno: {pct}")
            elif h=='Regular':
                self.assertTrue(0.40 <= pct < 0.60, f"Deuda incompatible para Regular: {pct}")
            elif h=='Malo':
                self.assertTrue(pct >= 0.60, f"Deuda incompatible para Malo: {pct}")

    def test_antiguedad_vs_edad(self):
        now_year = datetime.now().year
        for x in self.data:
            birth_year = int(x['fechaNacimiento'].split('-')[0])
            age = now_year - birth_year
            max_years = max(0, min(30, age - 18))
            self.assertTrue(0 <= x['antiguedadLaboral'] <= max_years, f"Antigüedad laboral inconsistente: {x['antiguedadLaboral']} (max {max_years})")

if __name__ == '__main__':
    unittest.main()
