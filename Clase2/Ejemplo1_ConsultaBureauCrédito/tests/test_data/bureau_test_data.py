"""
Datos de prueba para casos de Bureau de Crédito
"""

# TC-BC-001: Cliente con buen historial
CLIENTE_BUEN_HISTORIAL = {
    "documento": "1234567890",
    "tipo_documento": "CC",
    "expected_score_min": 700,
    "expected_estado": "APROBADO"
}

# TC-BC-002: Cliente con deudas activas al día
CLIENTE_DEUDAS_ACTIVAS = {
    "documento": "2345678901",
    "tipo_documento": "CC",
    "expected_score_min": 650,
    "expected_score_max": 699,
    "expected_estado": "REVISAR",
    "expected_deuda": 50000000
}

# TC-BC-003: Cliente con mora actual
CLIENTE_MOROSO = {
    "documento": "3456789012",
    "tipo_documento": "CC",
    "expected_score_max": 500,
    "expected_estado": "RECHAZADO",
    "expected_dias_mora_min": 1
}

# TC-BC-004: Cliente en lista CIFIN
CLIENTE_CIFIN = {
    "documento": "4567890123",
    "tipo_documento": "CC",
    "expected_estado": "RECHAZADO",
    "expected_en_cifin": True,
    "expected_razon": "Fraude 2023"
}

# TC-BC-005: Documento inválido (caracteres especiales)
DOCUMENTO_INVALIDO_CARACTERES = {
    "documento": "123-456*789",
    "tipo_documento": "CC",
    "expected_status": 422,
    "expected_error": "Documento inválido"
}

# TC-BC-006: Documento con longitud incorrecta
DOCUMENTO_LONGITUD_INCORRECTA = {
    "documento": "12345",
    "tipo_documento": "CC",
    "expected_status": 422,
    "expected_error": "Longitud inválida"
}

# TC-BC-007: Tipo de documento no válido
TIPO_DOCUMENTO_INVALIDO = {
    "documento": "1234567890",
    "tipo_documento": "XXX",
    "expected_status": 422,
    "expected_error": "Tipo documento no válido"
}

# TC-BC-010: Cliente extranjero con pasaporte
CLIENTE_EXTRANJERO = {
    "documento": "AB123456",
    "tipo_documento": "PAS",
    "expected_status": 200,
    "expected_score": None,
    "expected_sin_historial_local": True
}

# TC-BC-011: Cliente sin historial crediticio
CLIENTE_SIN_HISTORIAL = {
    "documento": "6789012345",
    "tipo_documento": "CC",
    "expected_status": 200,
    "expected_score": None,
    "expected_historial_encontrado": False,
    "expected_estado": "REQUIERE_ANALISIS_MANUAL"
}

# TC-BC-012: Documento para consulta duplicada
DOCUMENTO_DUPLICADO = {
    "documento": "7890123456",
    "tipo_documento": "CC"
}

# TC-BC-013: Cliente para consulta histórica
CLIENTE_HISTORICO = {
    "cliente_id": "550e8400-e29b-41d4-a716-446655440000",
    "documento": "8901234567",
    "tipo_documento": "CC"
}

# TC-BC-014: Cliente con score límite
CLIENTE_SCORE_LIMITE = {
    "documento": "8901234567",
    "tipo_documento": "CC",
    "expected_score": 600,
    "expected_estado": "REVISAR",
    "expected_requiere_gerencia": True
}

# TC-BC-015: Campo documento null
DOCUMENTO_NULL = {
    "documento": None,
    "tipo_documento": "CC",
    "expected_status": 422,
    "expected_error": "Campo requerido"
}

# Tipos de documento válidos
TIPOS_DOCUMENTO_VALIDOS = ["CC", "CE", "NIT", "PAS"]

# Estados válidos de respuesta
ESTADOS_VALIDOS = ["APROBADO", "RECHAZADO", "REVISAR", "REQUIERE_ANALISIS_MANUAL"]
