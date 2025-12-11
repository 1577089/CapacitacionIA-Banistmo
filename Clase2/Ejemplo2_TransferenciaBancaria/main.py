"""
API de Transferencias Bancarias - Ejercicio Práctico
Sistema de banca online con validaciones de límites, OTP y mantenimiento
"""
from datetime import datetime, time
from typing import Optional
from fastapi import FastAPI, HTTPException, Header, Request
from pydantic import BaseModel, Field, field_validator
import uvicorn
import threading

app = FastAPI(
    title="API Transferencias Bancarias",
    description="API REST para transferencias con validaciones de límites, seguridad y horarios",
    version="1.0.0"
)

# ==================== CONFIGURACIÓN ====================
LIMITE_DIARIO = 50000
LIMITE_MENSUAL = 5000000
MONTO_REQUIERE_OTP = 1000000
MANTENIMIENTO_INICIO = time(1, 0)  # 1:00 AM
MANTENIMIENTO_FIN = time(3, 0)     # 3:00 AM

# Mock de base de datos en memoria
cuentas_db = {
    "12345678": {"saldo": 100000, "estado": "ACTIVA", "transferido_hoy": 0, "transferido_mes": 0},
    "87654321": {"saldo": 50000, "estado": "ACTIVA", "transferido_hoy": 0, "transferido_mes": 0},
    "87654322": {"saldo": 30000, "estado": "ACTIVA", "transferido_hoy": 0, "transferido_mes": 0},
    "99999999": {"saldo": 10000, "estado": "BLOQUEADA", "transferido_hoy": 0, "transferido_mes": 0},
}

transferencias_historial = []
rate_limit_tracker = {}  # {cuenta: [(timestamp, count)]}

# Lock para transacciones atómicas (evitar race conditions)
db_lock = threading.Lock()

# OTP válido para testing (en producción vendría por SMS/email)
OTP_VALIDO = "123456"


# ==================== MODELOS ====================
class TransferenciaRequest(BaseModel):
    origen: str = Field(..., description="Número de cuenta origen", min_length=8, max_length=8)
    destino: str = Field(..., description="Número de cuenta destino", min_length=8, max_length=8)
    monto: float = Field(..., description="Monto a transferir", gt=0)
    otp: Optional[str] = Field(None, description="Código OTP para montos > $1,000,000")

    @field_validator('monto')
    @classmethod
    def validar_decimales(cls, v):
        # Permitir máximo 2 decimales
        if round(v, 2) != v:
            raise ValueError("El monto solo puede tener máximo 2 decimales")
        return v


class TransferenciaResponse(BaseModel):
    id: int
    origen: str
    destino: str
    monto: float
    status: str
    fecha: str
    mensaje: str
    saldo_restante: Optional[float] = None


# ==================== UTILIDADES ====================
def es_horario_mantenimiento(force_maintenance: bool = False) -> bool:
    """Verifica si estamos en ventana de mantenimiento"""
    if force_maintenance:
        return True
    
    ahora = datetime.now().time()
    return MANTENIMIENTO_INICIO <= ahora < MANTENIMIENTO_FIN


def validar_rate_limit(cuenta: str, max_ops: int = 10, ventana_segundos: int = 60) -> bool:
    """Validación simple de rate limiting"""
    from datetime import datetime, timedelta
    
    ahora = datetime.now()
    if cuenta not in rate_limit_tracker:
        rate_limit_tracker[cuenta] = []
    
    # Limpiar entradas antiguas
    rate_limit_tracker[cuenta] = [
        ts for ts in rate_limit_tracker[cuenta]
        if ahora - ts < timedelta(seconds=ventana_segundos)
    ]
    
    # Verificar límite
    if len(rate_limit_tracker[cuenta]) >= max_ops:
        return False
    
    rate_limit_tracker[cuenta].append(ahora)
    return True


# ==================== ENDPOINTS ====================
@app.get("/")
def root():
    return {"message": "API Transferencias Bancarias", "status": "online"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/api/transferencias", response_model=TransferenciaResponse)
async def crear_transferencia(
    transferencia: TransferenciaRequest,
    request: Request,
    authorization: Optional[str] = Header(None),
    x_otp: Optional[str] = Header(None),
    x_force_maintenance: Optional[str] = Header(None)
):
    """
    Crea una transferencia bancaria con validaciones completas
    
    Validaciones implementadas:
    - Límite diario: $50,000
    - Límite mensual: $5,000,000
    - OTP obligatorio para montos > $1,000,000
    - Saldo suficiente
    - Horario de mantenimiento (1AM-3AM)
    - Cuenta destino válida
    - Cuenta origen activa (no bloqueada)
    - Origen != Destino
    - Rate limiting
    """
    
    # 1. VALIDAR AUTENTICACIÓN
    if not authorization:
        raise HTTPException(status_code=401, detail="No autorizado - Token requerido")
    
    # 2. VALIDAR HORARIO DE MANTENIMIENTO
    force_maint = x_force_maintenance == "1" if x_force_maintenance else False
    if es_horario_mantenimiento(force_maint):
        raise HTTPException(
            status_code=503,
            detail="Sistema en mantenimiento. Intente entre 3:00 AM y 1:00 AM"
        )
    
    # 3. VALIDAR RATE LIMITING
    if not validar_rate_limit(transferencia.origen):
        raise HTTPException(
            status_code=429,
            detail="Demasiadas solicitudes. Intente más tarde"
        )
    
    # 4. VALIDAR ORIGEN != DESTINO
    if transferencia.origen == transferencia.destino:
        raise HTTPException(
            status_code=400,
            detail="La cuenta origen no puede ser igual a la cuenta destino"
        )
    
    # 5. VALIDAR CUENTA ORIGEN EXISTE
    if transferencia.origen not in cuentas_db:
        raise HTTPException(status_code=404, detail="Cuenta origen no encontrada")
    
    cuenta_origen = cuentas_db[transferencia.origen]
    
    # 6. VALIDAR CUENTA NO BLOQUEADA
    if cuenta_origen["estado"] == "BLOQUEADA":
        raise HTTPException(
            status_code=403,
            detail="Cuenta bloqueada. Contacte al banco"
        )
    
    # 7. VALIDAR CUENTA DESTINO EXISTE
    if transferencia.destino not in cuentas_db:
        raise HTTPException(status_code=404, detail="Cuenta destino no encontrada")
    
    # 8. VALIDAR MONTO NEGATIVO (ya validado por Pydantic gt=0)
    if transferencia.monto <= 0:
        raise HTTPException(status_code=400, detail="El monto debe ser mayor a cero")
    
    # 9. VALIDAR OTP PARA MONTOS ALTOS
    if transferencia.monto > MONTO_REQUIERE_OTP:
        otp_enviado = x_otp or transferencia.otp
        if not otp_enviado or otp_enviado != OTP_VALIDO:
            raise HTTPException(
                status_code=401,
                detail=f"OTP inválido o ausente. Requerido para montos > ${MONTO_REQUIERE_OTP:,.0f}"
            )
    
    # 10. VALIDAR SALDO SUFICIENTE
    if cuenta_origen["saldo"] < transferencia.monto:
        raise HTTPException(
            status_code=402,
            detail=f"Saldo insuficiente. Disponible: ${cuenta_origen['saldo']:,.2f}"
        )
    
    # 11. VALIDAR LÍMITE DIARIO
    if cuenta_origen["transferido_hoy"] + transferencia.monto > LIMITE_DIARIO:
        raise HTTPException(
            status_code=403,
            detail=f"Excede límite diario de ${LIMITE_DIARIO:,.0f}. Usado hoy: ${cuenta_origen['transferido_hoy']:,.2f}"
        )
    
    # 12. VALIDAR LÍMITE MENSUAL
    if cuenta_origen["transferido_mes"] + transferencia.monto > LIMITE_MENSUAL:
        raise HTTPException(
            status_code=403,
            detail=f"Excede límite mensual de ${LIMITE_MENSUAL:,.0f}. Usado este mes: ${cuenta_origen['transferido_mes']:,.2f}"
        )
    
    # ==================== PROCESAR TRANSFERENCIA ====================
    # Simular transacción atómica con lock para evitar race conditions
    with db_lock:
        # Re-verificar saldo dentro del lock (double-check locking pattern)
        if cuentas_db[transferencia.origen]["saldo"] < transferencia.monto:
            raise HTTPException(
                status_code=402,
                detail=f"Saldo insuficiente. Disponible: ${cuentas_db[transferencia.origen]['saldo']:,.2f}"
            )
        
        try:
            # Debitar cuenta origen
            cuentas_db[transferencia.origen]["saldo"] -= transferencia.monto
            cuentas_db[transferencia.origen]["transferido_hoy"] += transferencia.monto
            cuentas_db[transferencia.origen]["transferido_mes"] += transferencia.monto
            
            # Acreditar cuenta destino
            cuentas_db[transferencia.destino]["saldo"] += transferencia.monto
            
            # Guardar en historial
            transferencia_id = len(transferencias_historial) + 1
            registro = {
                "id": transferencia_id,
                "origen": transferencia.origen,
                "destino": transferencia.destino,
                "monto": transferencia.monto,
                "fecha": datetime.now().isoformat(),
                "status": "COMPLETED"
            }
            transferencias_historial.append(registro)
            
            return TransferenciaResponse(
                id=transferencia_id,
                origen=transferencia.origen,
                destino=transferencia.destino,
                monto=transferencia.monto,
                status="COMPLETED",
                fecha=registro["fecha"],
                mensaje="Transferencia realizada exitosamente",
                saldo_restante=cuentas_db[transferencia.origen]["saldo"]
            )
            
        except Exception as e:
            # Rollback en caso de error
            raise HTTPException(status_code=500, detail=f"Error procesando transferencia: {str(e)}")


@app.get("/api/transferencias/historial")
def obtener_historial():
    """Obtiene el historial de todas las transferencias"""
    return {"transferencias": transferencias_historial, "total": len(transferencias_historial)}


@app.get("/api/cuentas/{numero_cuenta}")
def obtener_cuenta(numero_cuenta: str):
    """Obtiene información de una cuenta"""
    if numero_cuenta not in cuentas_db:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    
    return {
        "numero": numero_cuenta,
        **cuentas_db[numero_cuenta]
    }


@app.post("/api/cuentas/{numero_cuenta}/reset")
def resetear_cuenta(numero_cuenta: str):
    """Resetea los límites diarios y mensuales (solo para testing)"""
    if numero_cuenta not in cuentas_db:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    
    cuentas_db[numero_cuenta]["transferido_hoy"] = 0
    cuentas_db[numero_cuenta]["transferido_mes"] = 0
    cuentas_db[numero_cuenta]["saldo"] = 100000  # Reset saldo inicial
    
    return {"mensaje": "Cuenta reseteada", "cuenta": cuentas_db[numero_cuenta]}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
