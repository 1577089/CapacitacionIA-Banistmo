"""
Configuración de fixtures para pytest
"""
import pytest
import os
from dotenv import load_dotenv
from tests.helpers.api_client import BureauAPIClient

load_dotenv()


@pytest.fixture(scope="session")
def api_base_url():
    """URL base del API"""
    return os.getenv("API_BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="session")
def api_timeout():
    """Timeout para requests del API"""
    return int(os.getenv("API_TIMEOUT", "5"))


@pytest.fixture(scope="function")
def api_client(api_base_url, api_timeout):
    """Cliente del API Bureau - se crea nuevo para cada test"""
    client = BureauAPIClient(base_url=api_base_url, timeout=api_timeout)
    yield client
    client.close()


@pytest.fixture(scope="session")
def api_client_session(api_base_url, api_timeout):
    """Cliente del API Bureau - persiste durante toda la sesión"""
    client = BureauAPIClient(base_url=api_base_url, timeout=api_timeout)
    yield client
    client.close()


@pytest.fixture(scope="function")
def verificar_api_disponible(api_client):
    """
    Verifica que el API esté disponible antes de ejecutar el test
    Si el API no responde, marca el test como skipped
    """
    try:
        response = api_client.health_check()
        if response.status_code != 200:
            pytest.skip("API no está disponible")
    except Exception as e:
        pytest.skip(f"API no responde: {str(e)}")


@pytest.fixture(scope="function")
def limpiar_cache_bureau():
    """
    Fixture para limpiar caché entre tests si es necesario
    """
    # Implementar lógica de limpieza si el API lo soporta
    yield
    # Cleanup después del test


def pytest_configure(config):
    """Configuración inicial de pytest"""
    # Registrar markers personalizados
    config.addinivalue_line(
        "markers", "critical: casos críticos P0 (bloqueantes)"
    )
    config.addinivalue_line(
        "markers", "high: casos de alta prioridad P1"
    )
    config.addinivalue_line(
        "markers", "medium: casos de prioridad media P2"
    )


def pytest_collection_modifyitems(config, items):
    """Modificar items de test después de la recolección"""
    # Agregar marker 'smoke' a tests críticos automáticamente
    for item in items:
        if "critical" in item.keywords:
            item.add_marker(pytest.mark.smoke)
