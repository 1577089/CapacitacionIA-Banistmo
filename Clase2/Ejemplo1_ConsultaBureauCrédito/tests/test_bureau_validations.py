"""
Tests para validaciones de entrada
TC-BC-005, TC-BC-006, TC-BC-007
"""
import pytest
from tests.test_data.bureau_test_data import (
    DOCUMENTO_INVALIDO_CARACTERES,
    DOCUMENTO_LONGITUD_INCORRECTA,
    TIPO_DOCUMENTO_INVALIDO
)


class TestBureauValidations:
    """Suite de pruebas para validaciones de entrada"""
    
    @pytest.mark.high
    @pytest.mark.validation
    @pytest.mark.regression
    def test_tc_bc_005_documento_invalido_caracteres_especiales(self, api_client, verificar_api_disponible):
        """
        TC-BC-005: Validación documento de identidad inválido
        
        Precondiciones:
        - Sistema activo
        
        Resultado esperado:
        - Status 422 (Validation Error)
        - Mensaje: "Documento inválido"
        - No consulta Bureau
        - Log de validación
        """
        # Act
        response = api_client.consultar_bureau(
            documento=DOCUMENTO_INVALIDO_CARACTERES["documento"],
            tipo_documento=DOCUMENTO_INVALIDO_CARACTERES["tipo_documento"]
        )
        
        # Assert
        assert response.status_code == DOCUMENTO_INVALIDO_CARACTERES["expected_status"], \
            f"Status code esperado {DOCUMENTO_INVALIDO_CARACTERES['expected_status']}, recibido: {response.status_code}"
        
        data = response.json()
        assert "detail" in data or "message" in data or "error" in data, \
            "Respuesta debe contener mensaje de error"
        
        # Verificar que el mensaje indica documento inválido
        error_message = str(data).lower()
        assert any(keyword in error_message for keyword in ["documento", "invalid", "inválido"]), \
            f"Mensaje de error no indica problema con documento: {data}"
    
    @pytest.mark.high
    @pytest.mark.validation
    @pytest.mark.regression
    def test_tc_bc_006_documento_longitud_incorrecta(self, api_client, verificar_api_disponible):
        """
        TC-BC-006: Validación documento con longitud incorrecta
        
        Precondiciones:
        - Sistema activo
        
        Resultado esperado:
        - Status 422
        - Error: "Longitud inválida"
        - Rango esperado: 6-12 dígitos
        """
        # Act
        response = api_client.consultar_bureau(
            documento=DOCUMENTO_LONGITUD_INCORRECTA["documento"],
            tipo_documento=DOCUMENTO_LONGITUD_INCORRECTA["tipo_documento"]
        )
        
        # Assert
        assert response.status_code == DOCUMENTO_LONGITUD_INCORRECTA["expected_status"], \
            f"Status code esperado {DOCUMENTO_LONGITUD_INCORRECTA['expected_status']}, recibido: {response.status_code}"
        
        data = response.json()
        assert "detail" in data or "message" in data or "error" in data, \
            "Respuesta debe contener mensaje de error"
        
        # Verificar que el mensaje indica problema de longitud
        error_message = str(data).lower()
        assert any(keyword in error_message for keyword in ["longitud", "length", "corto", "short", "dígitos", "characters"]), \
            f"Mensaje de error no indica problema de longitud: {data}"
    
    @pytest.mark.high
    @pytest.mark.validation
    @pytest.mark.regression
    def test_tc_bc_007_tipo_documento_invalido(self, api_client, verificar_api_disponible):
        """
        TC-BC-007: Tipo de documento no válido
        
        Precondiciones:
        - Sistema activo
        
        Resultado esperado:
        - Status 422
        - Error: "Tipo documento no válido"
        - Tipos válidos: CC, CE, NIT, PAS
        """
        # Act
        response = api_client.consultar_bureau(
            documento=TIPO_DOCUMENTO_INVALIDO["documento"],
            tipo_documento=TIPO_DOCUMENTO_INVALIDO["tipo_documento"]
        )
        
        # Assert
        assert response.status_code == TIPO_DOCUMENTO_INVALIDO["expected_status"], \
            f"Status code esperado {TIPO_DOCUMENTO_INVALIDO['expected_status']}, recibido: {response.status_code}"
        
        data = response.json()
        assert "detail" in data or "message" in data or "error" in data, \
            "Respuesta debe contener mensaje de error"
        
        # Verificar que el mensaje indica tipo de documento inválido
        error_message = str(data).lower()
        assert any(keyword in error_message for keyword in ["tipo", "type", "documento", "document"]), \
            f"Mensaje de error no indica problema con tipo de documento: {data}"
    
    @pytest.mark.high
    @pytest.mark.validation
    def test_tc_bc_005_documento_vacio(self, api_client, verificar_api_disponible):
        """
        Test adicional: Documento vacío
        
        Resultado esperado:
        - Status 422
        - Error de validación
        """
        # Act
        response = api_client.consultar_bureau(
            documento="",
            tipo_documento="CC"
        )
        
        # Assert
        assert response.status_code == 422, \
            f"Status code esperado 422 para documento vacío, recibido: {response.status_code}"
    
    @pytest.mark.high
    @pytest.mark.validation
    def test_tc_bc_006_documento_solo_espacios(self, api_client, verificar_api_disponible):
        """
        Test adicional: Documento con solo espacios
        
        Resultado esperado:
        - Status 422
        - Error de validación
        """
        # Act
        response = api_client.consultar_bureau(
            documento="   ",
            tipo_documento="CC"
        )
        
        # Assert
        assert response.status_code == 422, \
            f"Status code esperado 422 para documento con espacios, recibido: {response.status_code}"
    
    @pytest.mark.high
    @pytest.mark.validation
    def test_tc_bc_007_tipo_documento_vacio(self, api_client, verificar_api_disponible):
        """
        Test adicional: Tipo de documento vacío
        
        Resultado esperado:
        - Status 422
        - Error de validación
        """
        # Act
        response = api_client.consultar_bureau(
            documento="1234567890",
            tipo_documento=""
        )
        
        # Assert
        assert response.status_code == 422, \
            f"Status code esperado 422 para tipo documento vacío, recibido: {response.status_code}"
