"""
Configuración de pytest para generar reportes SVE automáticamente.
"""

import pytest
import time
from .sve_reporter import SVEReporter


# Mapeo de test cases a IDs y metadatos
TEST_METADATA = {
    "test_01_transferencia_exitosa": {
        "id": "TC-01",
        "scenario": "Transferencia exitosa con datos válidos",
        "expected": "HTTP 200, estado COMPLETED, saldo actualizado",
        "preconditions": "Cuentas válidas, saldo suficiente, token válido"
    },
    "test_02_sin_autenticacion": {
        "id": "TC-02",
        "scenario": "Transferencia sin token de autenticación",
        "expected": "HTTP 401 Unauthorized",
        "preconditions": "Endpoint disponible, sin token"
    },
    "test_03_cuenta_origen_invalida": {
        "id": "TC-03",
        "scenario": "Cuenta origen no existe",
        "expected": "HTTP 404 o 400, mensaje de error",
        "preconditions": "Cuenta origen inexistente, token válido"
    },
    "test_04_cuenta_destino_invalida": {
        "id": "TC-04",
        "scenario": "Cuenta destino no existe",
        "expected": "HTTP 404 o 400, mensaje de error",
        "preconditions": "Cuenta destino inexistente, token válido"
    },
    "test_05_saldo_insuficiente": {
        "id": "TC-05",
        "scenario": "Saldo insuficiente para transferencia",
        "expected": "HTTP 400 o 402, mensaje de saldo insuficiente",
        "preconditions": "Monto mayor al saldo disponible"
    },
    "test_06_horario_mantenimiento": {
        "id": "TC-06",
        "scenario": "Transferencia en horario de mantenimiento",
        "expected": "HTTP 503 Service Unavailable",
        "preconditions": "Horario 1AM-3AM o variable FORCE_MAINTENANCE"
    },
    "test_07_monto_negativo": {
        "id": "TC-07",
        "scenario": "Intento de transferencia con monto negativo",
        "expected": "HTTP 400 o 422, validación de monto",
        "preconditions": "Monto < 0"
    },
    "test_08_excede_limite_diario": {
        "id": "TC-08",
        "scenario": "Transferencia excede límite diario de $50,000",
        "expected": "HTTP 403 Forbidden, mensaje de límite diario",
        "preconditions": "Monto > $50,000 o suma diaria > $50,000"
    },
    "test_09_excede_limite_mensual": {
        "id": "TC-09",
        "scenario": "Transferencia excede límite mensual de $5,000,000",
        "expected": "HTTP 403 Forbidden, mensaje de límite mensual",
        "preconditions": "Suma mensual > $5,000,000"
    },
    "test_10_otp_requerido": {
        "id": "TC-10",
        "scenario": "Transferencia >$1M sin OTP",
        "expected": "HTTP 401 o 403, mensaje OTP requerido",
        "preconditions": "Monto > $1,000,000, sin OTP"
    },
    "test_11_concurrencia": {
        "id": "TC-11",
        "scenario": "Dos transferencias simultáneas",
        "expected": "Una exitosa, otra rechazada por límite/saldo",
        "preconditions": "2 threads, transferencias que exceden límite total"
    },
    "test_12_cuenta_bloqueada": {
        "id": "TC-12",
        "scenario": "Transferencia desde cuenta bloqueada",
        "expected": "HTTP 403 Forbidden, mensaje cuenta bloqueada",
        "preconditions": "Cuenta en estado bloqueado"
    },
    "test_13_rate_limit": {
        "id": "TC-13",
        "scenario": "Exceder límite de 10 requests por minuto",
        "expected": "HTTP 429 Too Many Requests",
        "preconditions": "11+ requests en 60 segundos"
    },
    "test_14_mismo_origen_destino": {
        "id": "TC-14",
        "scenario": "Transferencia a la misma cuenta",
        "expected": "HTTP 400 Bad Request",
        "preconditions": "Cuenta origen == cuenta destino"
    },
    "test_15_validacion_campos": {
        "id": "TC-15",
        "scenario": "Campos requeridos faltantes o inválidos",
        "expected": "HTTP 422 Unprocessable Entity",
        "preconditions": "Request sin campos origen/destino/monto"
    }
}


sve_reporter = None


@pytest.fixture(scope="session", autouse=True)
def initialize_sve_reporter():
    """Inicializa el reporter SVE al inicio de la sesión de tests."""
    global sve_reporter
    sve_reporter = SVEReporter("API Transferencias Bancarias - Testing QA")
    yield
    # Al finalizar todos los tests, genera los reportes
    if sve_reporter and sve_reporter.test_results:
        files = sve_reporter.generate_all_formats("sve_report")
        print("\n" + "="*80)
        print("📊 REPORTES SVE GENERADOS:")
        print("="*80)
        for format_type, filepath in files.items():
            print(f"  ✅ {format_type.upper()}: {filepath}")
        print("="*80)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook para capturar resultados de cada test."""
    outcome = yield
    report = outcome.get_result()
    
    # Solo procesamos en la fase de call (ejecución real del test)
    if report.when == "call":
        test_name = item.name
        metadata = TEST_METADATA.get(test_name, {})
        
        # Determinar status
        if report.passed:
            status = "PASS"
            actual_result = "Test ejecutado exitosamente según lo esperado"
            error_msg = ""
        elif report.failed:
            status = "FAIL"
            actual_result = f"Test falló: {report.longreprtext}"
            error_msg = str(report.longrepr)
        elif report.skipped:
            status = "SKIP"
            actual_result = f"Test omitido: {report.longreprtext}"
            error_msg = ""
        else:
            status = "ERROR"
            actual_result = "Error inesperado durante ejecución"
            error_msg = str(report.longrepr) if hasattr(report, 'longrepr') else ""
        
        # Extraer datos de test si están disponibles
        test_data = {}
        if hasattr(item, 'funcargs'):
            test_data = {k: str(v) for k, v in item.funcargs.items() 
                        if not k.startswith('_')}
        
        # Agregar resultado al reporter
        if sve_reporter:
            sve_reporter.add_test_result(
                test_id=metadata.get("id", test_name),
                test_name=test_name,
                status=status,
                duration=report.duration,
                scenario=metadata.get("scenario", ""),
                expected_result=metadata.get("expected", ""),
                actual_result=actual_result,
                error_message=error_msg,
                preconditions=metadata.get("preconditions", ""),
                test_data=test_data
            )
