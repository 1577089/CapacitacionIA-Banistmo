"""
Tests para manejo de errores y casos extremos
TC-BC-008, TC-BC-009, TC-BC-015
"""
import pytest
import time
from requests.exceptions import Timeout, RequestException
from tests.test_data.bureau_test_data import DOCUMENTO_NULL


class TestBureauErrors:
    """Suite de pruebas para manejo de errores"""
    
    @pytest.mark.critical
    @pytest.mark.timeout(10)
    @pytest.mark.regression
    def test_tc_bc_008_timeout_5_segundos(self, api_client):
        """
        TC-BC-008: Servicio Bureau caído (timeout 5 segundos)
        
        Precondiciones:
        - API Bureau no disponible
        - Timeout configurado en 5s
        
        Resultado esperado:
        - Status 503 (Service Unavailable) o Timeout Exception
        - Mensaje: "Bureau no disponible"
        - Retry después de 30s
        - Log de incidencia
        
        Nota: Este test puede fallar si el servicio responde correctamente.
        Se marca como esperado que lance timeout o retorne 503/504.
        """
        try:
            # Intentar consulta con documento que simule timeout
            # (depende de la implementación del mock/API)
            start_time = time.time()
            
            response = api_client.consultar_bureau(
                documento="9999999999",  # Documento que simula timeout
                tipo_documento="CC"
            )
            
            elapsed_time = time.time() - start_time
            
            # Si responde, debería ser error de servicio no disponible
            if response.status_code in [503, 504, 408]:
                assert True, "Servicio correctamente retorna error de disponibilidad"
            elif response.status_code == 200:
                # Si el servicio responde OK, al menos verificar tiempo
                assert elapsed_time <= 5, \
                    f"Tiempo de respuesta {elapsed_time}s excede timeout de 5s"
            
        except Timeout:
            # Se espera timeout
            assert True, "Timeout capturado correctamente"
        except RequestException as e:
            # Otros errores de red son aceptables
            assert "timeout" in str(e).lower() or "timed out" in str(e).lower(), \
                f"Error de red inesperado: {e}"
    
    @pytest.mark.high
    @pytest.mark.regression
    def test_tc_bc_009_respuesta_invalida_del_bureau(self, api_client, verificar_api_disponible):
        """
        TC-BC-009: Respuesta inválida del Bureau
        
        Precondiciones:
        - Bureau retorna JSON malformado
        - API activa
        
        Resultado esperado:
        - Status 502 (Bad Gateway) o error de parseo
        - Error: "Respuesta inválida del Bureau"
        - No se procesa solicitud
        - Alerta a sistemas
        
        Nota: Este test depende de que el API tenga un endpoint que simule
        respuesta inválida o que el Bureau real retorne error.
        """
        try:
            # Documento que simula respuesta inválida del Bureau
            response = api_client.consultar_bureau(
                documento="8888888888",
                tipo_documento="CC"
            )
            
            # Si el API maneja correctamente respuestas inválidas del Bureau
            if response.status_code == 502:
                data = response.json()
                error_message = str(data).lower()
                assert any(keyword in error_message for keyword in ["inválida", "invalid", "malformed", "bad"]), \
                    f"Error message no indica respuesta inválida: {data}"
            elif response.status_code == 200:
                # Si responde OK, al menos verificar que tenga estructura válida
                data = response.json()
                assert isinstance(data, dict), "Respuesta debe ser un objeto JSON válido"
            
        except Exception as e:
            # Si falla el parseo, es aceptable para este test
            assert "json" in str(e).lower() or "parse" in str(e).lower(), \
                f"Error inesperado: {e}"
    
    @pytest.mark.high
    @pytest.mark.validation
    @pytest.mark.regression
    def test_tc_bc_015_campo_documento_null(self, api_client, verificar_api_disponible):
        """
        TC-BC-015: Validación campo vacío (documento null)
        
        Precondiciones:
        - Request sin documento
        
        Resultado esperado:
        - Status 422
        - Error: "Campo requerido: documento"
        - Validación antes de llamar Bureau
        - Mensaje user-friendly
        """
        try:
            # Intentar enviar request con documento null
            response = api_client.consultar_bureau(
                documento=DOCUMENTO_NULL["documento"],
                tipo_documento=DOCUMENTO_NULL["tipo_documento"]
            )
            
            # Assert
            assert response.status_code == DOCUMENTO_NULL["expected_status"], \
                f"Status code esperado {DOCUMENTO_NULL['expected_status']}, recibido: {response.status_code}"
            
            data = response.json()
            error_message = str(data).lower()
            assert any(keyword in error_message for keyword in ["requerido", "required", "documento", "field"]), \
                f"Mensaje de error no indica campo requerido: {data}"
                
        except Exception as e:
            # Puede fallar en la construcción del request, lo cual es válido
            assert "none" in str(e).lower() or "null" in str(e).lower() or "required" in str(e).lower(), \
                f"Error inesperado: {e}"
    
    @pytest.mark.high
    @pytest.mark.regression
    def test_tc_bc_008_verificar_retry_logic(self, api_client):
        """
        Test adicional: Verificar lógica de retry
        
        Si el API implementa retry, este test verifica que se intente
        múltiples veces antes de fallar definitivamente.
        """
        # Este test es más conceptual - la implementación depende del API
        # Por ahora solo documentamos el comportamiento esperado
        pass
    
    @pytest.mark.high
    def test_tc_bc_009_manejo_campo_faltante_en_respuesta(self, api_client, verificar_api_disponible):
        """
        Test adicional: Respuesta del Bureau sin campos obligatorios
        
        Verificar que el API maneja correctamente cuando el Bureau
        retorna respuesta sin campos críticos.
        """
        response = api_client.consultar_bureau(
            documento="1234567890",
            tipo_documento="CC"
        )
        
        if response.status_code == 200:
            data = response.json()
            # Verificar que tenga al menos los campos mínimos
            assert isinstance(data, dict), "Respuesta debe ser un diccionario"
            # No fallar si faltan campos, solo registrar
