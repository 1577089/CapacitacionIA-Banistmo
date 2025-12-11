import pytest
import sqlite3
import os
from datetime import datetime

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
DB_FILE = "test_db.sqlite"
SQL_FILE_PATH = 'carga_transacciones.sql'

# --- DDL para SQLite ---
TABLE_DDL = """
CREATE TABLE transacciones (
    id_transaccion TEXT PRIMARY KEY,
    fecha_hora TEXT NOT NULL,
    id_cuenta_origen TEXT NOT NULL,
    id_cuenta_destino TEXT,
    tipo_transaccion TEXT NOT NULL,
    monto REAL NOT NULL,
    estado TEXT NOT NULL,
    canal TEXT NOT NULL,
    descripcion TEXT,
    CONSTRAINT chk_monto_positivo CHECK (monto > 0),
    CONSTRAINT chk_cuentas_diferentes CHECK (id_cuenta_origen <> id_cuenta_destino)
);
"""

# --- FIXTURES DE PYTEST ---

@pytest.fixture(scope="module")
def db_connection():
    """Fixture para crear una BD SQLite, cargar datos y limpiarla después."""
    # Eliminar la BD anterior si existe para una prueba limpia
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cursor = conn.cursor()
        
        # Crear la tabla
        print("\nCreando tabla 'transacciones' en SQLite...")
        cursor.execute(TABLE_DDL)
        conn.commit()
        
        # Ejecutar el script de carga
        print(f"Cargando datos desde {SQL_FILE_PATH}...")
        with open(SQL_FILE_PATH, 'r', encoding='utf-8') as f:
            # SQLite no soporta ejecutar múltiples sentencias en un solo .execute()
            # por defecto con la librería estándar, así que usamos executescript()
            sql_script = f.read()
            cursor.executescript(sql_script)
        conn.commit()
        print("Carga de datos completada.")
        
        yield conn
        
    except sqlite3.Error as e:
        pytest.fail(f"Ocurrió un error con la base de datos SQLite. Error: {e}")
    finally:
        if conn:
            conn.close()
        # Limpieza final
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)

@pytest.fixture(scope="module")
def db_cursor(db_connection):
    """Fixture que proporciona un cursor para ejecutar queries."""
    db_connection.text_factory = str
    cursor = db_connection.cursor()
    yield cursor
    cursor.close()

# --- CASOS DE PRUEBA POSITIVOS (CP-001 a CP-008) ---

def test_cp001_carga_exitosa_y_cp002_conteo_registros(db_cursor):
    """Test para CP-001 y CP-002: Verifica la carga y el conteo total de registros."""
    db_cursor.execute("SELECT COUNT(*) FROM transacciones;")
    count = db_cursor.fetchone()[0]
    assert count == 10000, f"Se esperaban 10000 registros, pero se encontraron {count}."

def test_cp003_validacion_integridad_datos(db_cursor):
    """Test para CP-003: Valida los formatos de los IDs y tipos de datos en una muestra."""
    db_cursor.execute("SELECT id_transaccion, fecha_hora, monto, id_cuenta_origen, id_cuenta_destino FROM transacciones LIMIT 100;")
    sample = db_cursor.fetchall()
    for row in sample:
        id_transaccion, fecha_hora_str, monto, id_cuenta_origen, id_cuenta_destino = row
        assert id_transaccion.startswith("TRX-")
        # Validar que la fecha sea un string con el formato correcto
        assert isinstance(fecha_hora_str, str)
        datetime.strptime(fecha_hora_str, '%Y-%m-%d %H:%M:%S') # Lanza excepción si el formato es incorrecto
        assert isinstance(monto, float)
        assert id_cuenta_origen.startswith("ACC-")
        if id_cuenta_destino:
            assert id_cuenta_destino.startswith("ACC-")

def test_cp004_validacion_distribucion(db_cursor):
    """Test para CP-004: Valida la distribución aproximada de tipos, estados y canales."""
    total = 10000
    # Tipo de transacción
    db_cursor.execute("SELECT COUNT(*) FROM transacciones WHERE tipo_transaccion = 'TRANSFERENCIA';")
    assert total * 0.38 < db_cursor.fetchone()[0] < total * 0.42 # Margen de +/- 2%
    # Estado
    db_cursor.execute("SELECT COUNT(*) FROM transacciones WHERE estado = 'EXITOSA';")
    assert total * 0.83 < db_cursor.fetchone()[0] < total * 0.87 # Margen de +/- 2%
    # Canal
    db_cursor.execute("SELECT COUNT(*) FROM transacciones WHERE canal = 'APP_MOVIL';")
    assert total * 0.48 < db_cursor.fetchone()[0] < total * 0.52 # Margen de +/- 2%

def test_cp005_validacion_regla_cuentas(db_cursor):
    """Test para CP-005: Verifica que no haya transferencias a la misma cuenta y que depósitos/retiros no tengan destino."""
    db_cursor.execute("SELECT COUNT(*) FROM transacciones WHERE tipo_transaccion = 'TRANSFERENCIA' AND id_cuenta_origen = id_cuenta_destino;")
    assert db_cursor.fetchone()[0] == 0
    db_cursor.execute("SELECT COUNT(*) FROM transacciones WHERE tipo_transaccion IN ('DEPOSITO', 'RETIRO') AND id_cuenta_destino IS NOT NULL;")
    assert db_cursor.fetchone()[0] == 0

def test_cp006_validacion_limite_diario(db_cursor):
    """Test para CP-006: Verifica que ninguna cuenta exceda las 50 transacciones diarias."""
    db_cursor.execute("""
        SELECT COUNT(*) 
        FROM (
            SELECT id_cuenta_origen, DATE(fecha_hora)
            FROM transacciones 
            GROUP BY id_cuenta_origen, DATE(fecha_hora) 
            HAVING COUNT(*) > 50
        ) as subquery;
    """)
    assert db_cursor.fetchone()[0] == 0, "Se encontraron cuentas que exceden el límite de 50 transacciones diarias."

def test_cp007_validacion_rangos_montos(db_cursor):
    """Test para CP-007: Verifica que los montos estén en los rangos correctos."""
    rangos = {
        'TRANSFERENCIA': (10000, 5000000),
        'DEPOSITO': (20000, 10000000),
        'RETIRO': (10000, 3000000),
        'PAGO_SERVICIO': (5000, 500000)
    }
    for tipo, (min_monto, max_monto) in rangos.items():
        db_cursor.execute(f"SELECT COUNT(*) FROM transacciones WHERE tipo_transaccion = '{tipo}' AND (monto < {min_monto} OR monto > {max_monto});")
        assert db_cursor.fetchone()[0] == 0, f"Se encontraron montos fuera de rango para el tipo '{tipo}'."

# --- CASOS DE PRUEBA NEGATIVOS (CN-001 a CN-003) ---

def test_cn001_error_id_duplicado():
    """Test para CN-001: Intenta insertar un ID de transacción duplicado."""
    # Se necesita una conexión separada para no interferir con la fixture principal
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        # Obtener un ID existente
        cursor.execute("SELECT id_transaccion FROM transacciones LIMIT 1;")
        existing_id = cursor.fetchone()[0]
        
        # Intentar insertar un registro con el mismo ID
        with pytest.raises(sqlite3.IntegrityError) as excinfo:
            cursor.execute(f"INSERT INTO transacciones (id_transaccion, fecha_hora, id_cuenta_origen, tipo_transaccion, monto, estado, canal, descripcion) VALUES ('{existing_id}', '2025-01-01 12:00:00', 'ACC-00001', 'RETIRO', 50000, 'EXITOSA', 'CAJERO', 'Test duplicado');")
        
        assert "UNIQUE constraint failed: transacciones.id_transaccion" in str(excinfo.value)
    finally:
        conn.close()

def test_cn002_error_check_constraint_monto():
    """Test para CN-002: Verifica la restricción CHECK para montos no positivos."""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        # Este test ahora verifica que la restricción CHECK (monto > 0) funciona correctamente.
        with pytest.raises(sqlite3.IntegrityError) as excinfo:
             cursor.execute("INSERT INTO transacciones (id_transaccion, fecha_hora, id_cuenta_origen, tipo_transaccion, monto, estado, canal, descripcion) VALUES ('TRX-TEST-001', '2025-01-01 12:00:00', 'ACC-00001', 'RETIRO', 0, 'EXITOSA', 'CAJERO', 'Test monto cero');")
        
        assert "CHECK constraint failed: chk_monto_positivo" in str(excinfo.value)
    finally:
        if conn:
            conn.close()


def test_cn003_error_valor_nulo_obligatorio():
    """Test para CN-003: Intenta insertar NULL en un campo NOT NULL."""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        with pytest.raises(sqlite3.IntegrityError) as excinfo:
            cursor.execute("INSERT INTO transacciones (id_transaccion, fecha_hora, id_cuenta_origen, tipo_transaccion, monto, estado, canal, descripcion) VALUES ('TRX-TEST-002', '2025-01-01 12:00:00', NULL, 'RETIRO', 50000, 'EXITOSA', 'CAJERO', 'Test nulo');")
        
        assert "NOT NULL constraint failed: transacciones.id_cuenta_origen" in str(excinfo.value)
    finally:
        if conn:
            conn.close()

# --- Para ejecutar los tests, usa el comando `pytest` en tu terminal ---

