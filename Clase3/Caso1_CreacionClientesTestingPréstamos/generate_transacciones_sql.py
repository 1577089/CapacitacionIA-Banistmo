#!/usr/bin/env python3
"""
Generador de 10,000 INSERTs para la tabla `transacciones` (PostgreSQL).

Salida: archivo `transacciones_10000.sql` en el mismo directorio.

Uso:
  python generate_transacciones_sql.py

Parámetros opcionales (editar en el script):
  - SEED: semilla para reproducibilidad
  - N_TXNS: número de transacciones a generar
"""
import random
import datetime
from decimal import Decimal
from collections import defaultdict
import os

# Configuración
SEED = 42
N_TXNS = 10000
POOL_ACCOUNTS = 500
OUTFILE = "transacciones_10000.sql"

random.seed(SEED)

now = datetime.datetime.now()
end_dt = now
start_dt = now - datetime.timedelta(days=365 * 2)  # últimos 2 años
start_ts = int(start_dt.timestamp())
end_ts = int(end_dt.timestamp())

# Accounts pool ACC-00001 .. ACC-00500
accounts = [f"ACC-{i:05d}" for i in range(1, POOL_ACCOUNTS + 1)]

# Weighted choices
TIPOS = [
    ("TRANSFERENCIA", 0.40),
    ("DEPOSITO", 0.25),
    ("RETIRO", 0.20),
    ("PAGO_SERVICIO", 0.15),
]

CANAL = [("APP_MOVIL", 0.50), ("WEB", 0.30), ("CAJERO", 0.15), ("SUCURSAL", 0.05)]

ESTADOS = [("EXITOSA", 0.85), ("PENDIENTE", 0.10), ("RECHAZADA", 0.05)]

SERVICIOS = ["Agua", "Energía", "Internet", "Teléfono", "Seguro", "Impuesto"]

# Montos (min, max) por tipo
RANGES = {
    "TRANSFERENCIA": (10000.00, 5000000.00),
    "DEPOSITO": (20000.00, 10000000.00),
    "RETIRO": (10000.00, 3000000.00),
    "PAGO_SERVICIO": (5000.00, 500000.00),
}

def weighted_choice(choices):
    r = random.random()
    cum = 0.0
    for val, w in choices:
        cum += w
        if r <= cum:
            return val
    return choices[-1][0]


def generate_timestamps(n):
    # Uniform timestamps between start_ts and end_ts
    ts = [random.randint(start_ts, end_ts) for _ in range(n)]
    ts.sort()
    # add small random seconds within same day for variety
    return [datetime.datetime.fromtimestamp(t) for t in ts]


def format_ts(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def money_for(tipo):
    lo, hi = RANGES[tipo]
    # two decimals
    value = random.uniform(lo, hi)
    return f"{Decimal(value).quantize(Decimal('0.01'))}"


def descripcion_for(tipo, dest_account=None):
    if tipo == "TRANSFERENCIA":
        return f"Transferencia a {dest_account}"
    if tipo == "DEPOSITO":
        return "Depósito en efectivo"
    if tipo == "RETIRO":
        return "Retiro en efectivo"
    if tipo == "PAGO_SERVICIO":
        servicio = random.choice(SERVICIOS)
        return f"Pago {servicio}"
    return ""


def choose_accounts_for_transfer(date_str, counts):
    # pick origin and destination distinct and with counts < 50
    attempts = 0
    while attempts < 500:
        a = random.choice(accounts)
        b = random.choice(accounts)
        if a == b:
            attempts += 1
            continue
        if counts[(a, date_str)] >= 50 or counts[(b, date_str)] >= 50:
            attempts += 1
            continue
        return a, b
    # fallback: pick two accounts with minimal counts
    sorted_acc = sorted(accounts, key=lambda x: counts[(x, date_str)])
    return sorted_acc[0], sorted_acc[1] if sorted_acc[0] != sorted_acc[1] else sorted_acc[0]


def choose_account_single(date_str, counts):
    # pick account with counts < 50
    for _ in range(200):
        a = random.choice(accounts)
        if counts[(a, date_str)] < 50:
            return a
    # fallback: choose account with minimal count
    return min(accounts, key=lambda x: counts[(x, date_str)])


def main():
    timestamps = generate_timestamps(N_TXNS)

    counts = defaultdict(int)  # (account, date_str) -> count
    per_day_seq = defaultdict(int)  # date_str -> seq number for id_transaccion

    lines = []
    for idx, dt in enumerate(timestamps, start=1):
        date_str_day = dt.strftime("%Y%m%d")
        date_str_day_human = dt.strftime("%Y-%m-%d")
        per_day_seq[date_str_day] += 1
        seq = per_day_seq[date_str_day]
        trx_id = f"TRX-{date_str_day}-{seq:05d}"

        tipo = weighted_choice(TIPOS)

        # Estado: RECHAZADA only allowed for TRANSFERENCIA and RETIRO
        if tipo in ("TRANSFERENCIA", "RETIRO"):
            estado = weighted_choice(ESTADOS)
        else:
            # exclude RECHAZADA
            # normalize weights for EXITOSA and PENDIENTE
            p_exitosa = 0.85 / (0.85 + 0.10)
            p_pendiente = 0.10 / (0.85 + 0.10)
            estado = weighted_choice([("EXITOSA", p_exitosa), ("PENDIENTE", p_pendiente)])

        canal = weighted_choice(CANAL)
        monto = money_for(tipo)

        if tipo == "TRANSFERENCIA":
            origen, destino = choose_accounts_for_transfer(date_str_day, counts)
            # increment counts for both
            counts[(origen, date_str_day)] += 1
            counts[(destino, date_str_day)] += 1
            destino_sql = f"'{destino}'"
            desc = descripcion_for(tipo, dest_account=destino)
            origen_sql = f"'{origen}'"
        elif tipo == "DEPOSITO":
            origen = choose_account_single(date_str_day, counts)
            counts[(origen, date_str_day)] += 1
            destino_sql = "NULL"
            desc = descripcion_for(tipo)
            origen_sql = f"'{origen}'"
        elif tipo == "RETIRO":
            origen = choose_account_single(date_str_day, counts)
            counts[(origen, date_str_day)] += 1
            destino_sql = "NULL"
            desc = descripcion_for(tipo)
            origen_sql = f"'{origen}'"
        elif tipo == "PAGO_SERVICIO":
            origen = choose_account_single(date_str_day, counts)
            counts[(origen, date_str_day)] += 1
            destino_sql = "NULL"
            desc = descripcion_for(tipo)
            origen_sql = f"'{origen}'"
        else:
            origen_sql = "NULL"
            destino_sql = "NULL"
            desc = ""

        fecha_sql = f"'{format_ts(dt)}'"

        # Build INSERT
        # Columns: id_transaccion, fecha_hora, id_cuenta_origen, id_cuenta_destino, tipo_transaccion, monto, estado, canal, descripcion
        line = (
            "INSERT INTO transacciones (id_transaccion, fecha_hora, id_cuenta_origen, id_cuenta_destino, "
            "tipo_transaccion, monto, estado, canal, descripcion) VALUES ("
            f"'{trx_id}', {fecha_sql}, {origen_sql}, {destino_sql}, '{tipo}', {monto}, '{estado}', '{canal}', '{desc}');"
        )
        lines.append(line)

    # Write to file
    here = os.path.dirname(os.path.abspath(__file__))
    outpath = os.path.join(here, OUTFILE)
    with open(outpath, "w", encoding="utf-8") as f:
        f.write("-- Archivo generado por generate_transacciones_sql.py\n")
        f.write(f"-- Semilla={SEED}, registros={N_TXNS}\n")
        for l in lines:
            f.write(l + "\n")

    print(f"Generado {outpath} con {len(lines)} INSERTs")


if __name__ == "__main__":
    main()
