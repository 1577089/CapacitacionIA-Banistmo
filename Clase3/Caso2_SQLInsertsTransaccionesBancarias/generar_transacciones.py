import csv
import random
from datetime import datetime, timedelta

# --- CONFIGURACIÓN ---
NUM_TRANSACCIONES = 10000
NUM_CUENTAS = 500
FECHA_INICIO = datetime.now() - timedelta(days=2*365)
FECHA_FIN = datetime.now()

# --- POOLS DE DATOS ---
TIPOS_TRANSACCION = ['TRANSFERENCIA', 'DEPOSITO', 'RETIRO', 'PAGO_SERVICIO']
ESTADOS = ['EXITOSA', 'PENDIENTE', 'RECHAZADA']
CANALES = ['APP_MOVIL', 'WEB', 'CAJERO', 'SUCURSAL']
SERVICIOS = ['Energía', 'Agua', 'Internet', 'Telefonía', 'Gas']

# --- DISTRIBUCIONES ---
DIST_TIPO_TRANSACCION = [0.40, 0.25, 0.20, 0.15]
DIST_ESTADO = [0.85, 0.10, 0.05]
DIST_CANAL = [0.50, 0.30, 0.15, 0.05]

# --- RANGOS DE MONTO ---
RANGOS_MONTO = {
    'TRANSFERENCIA': (10000, 5000000),
    'DEPOSITO': (20000, 10000000),
    'RETIRO': (10000, 3000000),
    'PAGO_SERVICIO': (5000, 500000)
}

# --- GENERACIÓN DE CUENTAS ---
cuentas = [f"ACC-{str(i).zfill(5)}" for i in range(1, NUM_CUENTAS + 1)]

def generar_fecha_aleatoria(inicio, fin):
    """Genera una fecha y hora aleatoria en un rango."""
    delta = fin - inicio
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return inicio + timedelta(seconds=random_second)

def generar_transacciones():
    """Genera la lista de transacciones con datos sintéticos."""
    transacciones = []
    trans_por_cuenta_dia = {} # Para controlar el límite de 50 transacciones

    while len(transacciones) < NUM_TRANSACCIONES:
        tipo_transaccion = random.choices(TIPOS_TRANSACCION, weights=DIST_TIPO_TRANSACCION, k=1)[0]
        
        cuenta_origen = random.choice(cuentas)
        fecha_hora = generar_fecha_aleatoria(FECHA_INICIO, FECHA_FIN)
        fecha_str = fecha_hora.strftime('%Y-%m-%d')

        # Control de 50 transacciones por cuenta por día
        key = (cuenta_origen, fecha_str)
        if trans_por_cuenta_dia.get(key, 0) >= 50:
            continue # Se salta esta iteración si la cuenta ya alcanzó el límite para ese día

        monto = round(random.uniform(*RANGOS_MONTO[tipo_transaccion]), 2)
        canal = random.choices(CANALES, weights=DIST_CANAL, k=1)[0]
        
        # Lógica de estado
        if tipo_transaccion in ['TRANSFERENCIA', 'RETIRO']:
            estado = random.choices(ESTADOS, weights=DIST_ESTADO, k=1)[0]
        else: # DEPOSITO y PAGO_SERVICIO no pueden ser RECHAZADOS
            estado = random.choices(ESTADOS[:2], weights=[0.90, 0.10], k=1)[0] # Ajuste de pesos para Exitoso/Pendiente

        # Lógica de cuentas y descripción
        cuenta_destino = None
        if tipo_transaccion == 'TRANSFERENCIA':
            cuenta_destino = random.choice([c for c in cuentas if c != cuenta_origen])
            descripcion = f"Transferencia a cuenta {cuenta_destino}"
        elif tipo_transaccion == 'DEPOSITO':
            descripcion = "Depósito en efectivo"
        elif tipo_transaccion == 'RETIRO':
            descripcion = "Retiro de efectivo"
        elif tipo_transaccion == 'PAGO_SERVICIO':
            servicio = random.choice(SERVICIOS)
            descripcion = f"Pago servicio de {servicio}"

        transacciones.append({
            "fecha_hora": fecha_hora,
            "id_cuenta_origen": cuenta_origen,
            "id_cuenta_destino": cuenta_destino,
            "tipo_transaccion": tipo_transaccion,
            "monto": monto,
            "estado": estado,
            "canal": canal,
            "descripcion": descripcion
        })

        # Incrementar contador de transacciones para la cuenta/día
        trans_por_cuenta_dia[key] = trans_por_cuenta_dia.get(key, 0) + 1

    # Ordenar cronológicamente
    transacciones.sort(key=lambda x: x['fecha_hora'])

    # Generar ID de transacción después de ordenar
    for i, trx in enumerate(transacciones):
        fecha_id = trx['fecha_hora'].strftime('%Y%m%d')
        trx['id_transaccion'] = f"TRX-{fecha_id}-{str(i+1).zfill(5)}"

    return transacciones

def escribir_sql(transacciones):
    """Escribe las transacciones en un archivo .sql."""
    with open('carga_transacciones.sql', 'w', encoding='utf-8') as f:
        f.write("-- Archivo de carga masiva para la tabla 'transacciones'\n")
        f.write("-- Generado en: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n\n")
        
        for trx in transacciones:
            id_transaccion = trx['id_transaccion']
            fecha_hora = trx['fecha_hora'].strftime('%Y-%m-%d %H:%M:%S')
            id_cuenta_origen = trx['id_cuenta_origen']
            id_cuenta_destino = f"'{trx['id_cuenta_destino']}'" if trx['id_cuenta_destino'] else 'NULL'
            tipo_transaccion = trx['tipo_transaccion']
            monto = trx['monto']
            estado = trx['estado']
            canal = trx['canal']
            descripcion = trx['descripcion'].replace("'", "''") # Escapar comillas simples

            sql = (
                f"INSERT INTO transacciones (id_transaccion, fecha_hora, id_cuenta_origen, id_cuenta_destino, tipo_transaccion, monto, estado, canal, descripcion) "
                f"VALUES ('{id_transaccion}', '{fecha_hora}', '{id_cuenta_origen}', {id_cuenta_destino}, '{tipo_transaccion}', {monto}, '{estado}', '{canal}', '{descripcion}');\n"
            )
            f.write(sql)

if __name__ == "__main__":
    print("Iniciando generación de datos sintéticos...")
    lista_transacciones = generar_transacciones()
    print(f"Se generaron {len(lista_transacciones)} transacciones.")
    print("Escribiendo archivo 'carga_transacciones.sql'...")
    escribir_sql(lista_transacciones)
    print("¡Proceso completado! El archivo 'carga_transacciones.sql' está listo.")
