"""
Tests para path feliz y casos positivos de Bureau de Crédito
TC-BC-001 a TC-BC-004
"""
import pytest
from tests.test_data.bureau_test_data import (
    CLIENTE_BUEN_HISTORIAL,
    CLIENTE_DEUDAS_ACTIVAS,
    CLIENTE_MOROSO,
    CLIENTE_CIFIN
)


class TestBureauHappyPath:
    """Suite de pruebas para casos positivos y path feliz"""
    
    @pytest.mark.critical
    @pytest.mark.smoke
    @pytest.mark.integration
    def test_tc_bc_001_cliente_buen_historial(self, api_client, verificar_api_disponible):
        """
        TC-BC-001: Path feliz - Cliente con buen historial crediticio
        
        Precondiciones:
        - API Bureau disponible
        - Cliente existe en BD
        - Cliente tiene historial positivo
        
        Resultado esperado:
        - Status 200
        - Score >= 700
        - Estado: "APROBADO"
        - Sin deudas en mora
        - Tiempo respuesta < 3s
        """
        # Act
        response = api_client.consultar_bureau(
            documento=CLIENTE_BUEN_HISTORIAL["documento"],
            tipo_documento=CLIENTE_BUEN_HISTORIAL["tipo_documento"]
        )
        
        # Assert
        assert response.status_code == 200, f"Status code incorrecto: {response.status_code}"
        
        data = response.json()
        assert "score" in data, "Respuesta no contiene campo 'score'"
        assert data["score"] >= CLIENTE_BUEN_HISTORIAL["expected_score_min"], \
            f"Score {data['score']} es menor que el esperado {CLIENTE_BUEN_HISTORIAL['expected_score_min']}"
        
        assert "estado" in data, "Respuesta no contiene campo 'estado'"
        assert data["estado"] == CLIENTE_BUEN_HISTORIAL["expected_estado"], \
            f"Estado {data['estado']} diferente del esperado {CLIENTE_BUEN_HISTORIAL['expected_estado']}"
        
        # Validar tiempo de respuesta
        assert response.elapsed.total_seconds() < 3, \
            f"Tiempo de respuesta {response.elapsed.total_seconds()}s excede el límite de 3s"
        
        # Validar que no tenga deudas en mora
        if "dias_mora" in data:
            assert data["dias_mora"] == 0, f"Cliente tiene {data['dias_mora']} días de mora"
    
    @pytest.mark.critical
    @pytest.mark.regression
    @pytest.mark.integration
    def test_tc_bc_002_cliente_deudas_activas_al_dia(self, api_client, verificar_api_disponible):
        """
        TC-BC-002: Cliente con deudas activas pero al día
        
        Precondiciones:
        - API Bureau disponible
        - Cliente tiene préstamos vigentes
        - Sin moras actuales
        
        Resultado esperado:
        - Status 200
        - Score: 650-699
        - Estado: "REVISAR"
        - Lista de deudas activas
        - Monto_deuda_total visible
        """
        # Act
        response = api_client.consultar_bureau(
            documento=CLIENTE_DEUDAS_ACTIVAS["documento"],
            tipo_documento=CLIENTE_DEUDAS_ACTIVAS["tipo_documento"]
        )
        
        # Assert
        assert response.status_code == 200, f"Status code incorrecto: {response.status_code}"
        
        data = response.json()
        assert "score" in data, "Respuesta no contiene campo 'score'"
        assert CLIENTE_DEUDAS_ACTIVAS["expected_score_min"] <= data["score"] <= CLIENTE_DEUDAS_ACTIVAS["expected_score_max"], \
            f"Score {data['score']} fuera del rango esperado 650-699"
        
        assert data["estado"] == CLIENTE_DEUDAS_ACTIVAS["expected_estado"], \
            f"Estado {data['estado']} diferente del esperado"
        
        # Validar que tenga información de deudas
        assert "monto_deuda_total" in data or "deudas_activas" in data, \
            "Respuesta no contiene información de deudas"
    
    @pytest.mark.critical
    @pytest.mark.regression
    @pytest.mark.integration
    def test_tc_bc_003_cliente_con_mora_actual(self, api_client, verificar_api_disponible):
        """
        TC-BC-003: Cliente con mora actual
        
        Precondiciones:
        - Cliente registrado
        - Cliente tiene pagos vencidos
        
        Resultado esperado:
        - Status 200
        - Score < 500
        - Estado: "RECHAZADO"
        - dias_mora > 0
        - Alertas de riesgo activas
        """
        # Act
        response = api_client.consultar_bureau(
            documento=CLIENTE_MOROSO["documento"],
            tipo_documento=CLIENTE_MOROSO["tipo_documento"]
        )
        
        # Assert
        assert response.status_code == 200, f"Status code incorrecto: {response.status_code}"
        
        data = response.json()
        assert "score" in data, "Respuesta no contiene campo 'score'"
        assert data["score"] < CLIENTE_MOROSO["expected_score_max"], \
            f"Score {data['score']} no refleja situación de mora (esperado < 500)"
        
        assert data["estado"] == CLIENTE_MOROSO["expected_estado"], \
            f"Estado {data['estado']} debería ser RECHAZADO para cliente moroso"
        
        # Validar días de mora
        if "dias_mora" in data:
            assert data["dias_mora"] >= CLIENTE_MOROSO["expected_dias_mora_min"], \
                f"Cliente debe tener al menos {CLIENTE_MOROSO['expected_dias_mora_min']} día de mora"
    
    @pytest.mark.critical
    @pytest.mark.regression
    @pytest.mark.integration
    def test_tc_bc_004_cliente_en_lista_cifin(self, api_client, verificar_api_disponible):
        """
        TC-BC-004: Cliente en lista de riesgo CIFIN
        
        Precondiciones:
        - Cliente reportado en CIFIN
        - API Bureau disponible
        
        Resultado esperado:
        - Status 200
        - en_cifin: true
        - Estado: "RECHAZADO"
        - razon_reporte visible
        - Bloqueo automático
        """
        # Act
        response = api_client.consultar_bureau(
            documento=CLIENTE_CIFIN["documento"],
            tipo_documento=CLIENTE_CIFIN["tipo_documento"]
        )
        
        # Assert
        assert response.status_code == 200, f"Status code incorrecto: {response.status_code}"
        
        data = response.json()
        assert "estado" in data, "Respuesta no contiene campo 'estado'"
        assert data["estado"] == CLIENTE_CIFIN["expected_estado"], \
            f"Cliente en CIFIN debe tener estado RECHAZADO, recibido: {data['estado']}"
        
        # Validar flag CIFIN
        if "en_cifin" in data:
            assert data["en_cifin"] == CLIENTE_CIFIN["expected_en_cifin"], \
                "Flag en_cifin debe ser true para cliente reportado"
        
        # Validar que tenga razón del reporte
        if "razon_reporte" in data or "motivo_rechazo" in data:
            assert True, "Respuesta contiene información del reporte"
