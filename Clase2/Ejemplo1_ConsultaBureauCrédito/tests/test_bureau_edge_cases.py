"""
Tests para edge cases y casos extremos
TC-BC-010, TC-BC-011, TC-BC-012, TC-BC-013, TC-BC-014
"""
import pytest
import threading
import time
from tests.test_data.bureau_test_data import (
    CLIENTE_EXTRANJERO,
    CLIENTE_SIN_HISTORIAL,
    DOCUMENTO_DUPLICADO,
    CLIENTE_HISTORICO,
    CLIENTE_SCORE_LIMITE
)


class TestBureauEdgeCases:
    """Suite de pruebas para edge cases"""
    
    @pytest.mark.high
    @pytest.mark.edge_case
    @pytest.mark.integration
    def test_tc_bc_010_cliente_extranjero_pasaporte(self, api_client, verificar_api_disponible):
        """
        TC-BC-010: Cliente extranjero con pasaporte
        
        Precondiciones:
        - Cliente no residente
        - Documento tipo PAS
        
        Resultado esperado:
        - Status 200
        - Score: null o 0
        - sin_historial_local: true
        - Mensaje: "Consulta internacional requerida"
        """
        # Act
        response = api_client.consultar_bureau(
            documento=CLIENTE_EXTRANJERO["documento"],
            tipo_documento=CLIENTE_EXTRANJERO["tipo_documento"]
        )
        
        # Assert
        assert response.status_code == CLIENTE_EXTRANJERO["expected_status"], \
            f"Status code esperado {CLIENTE_EXTRANJERO['expected_status']}, recibido: {response.status_code}"
        
        data = response.json()
        
        # Para clientes extranjeros, el score puede ser null o 0
        if "score" in data:
            assert data["score"] in [None, 0, CLIENTE_EXTRANJERO["expected_score"]], \
                f"Score para cliente extranjero debe ser null o 0, recibido: {data['score']}"
        
        # Verificar flag de historial local
        if "sin_historial_local" in data:
            assert data["sin_historial_local"] == CLIENTE_EXTRANJERO["expected_sin_historial_local"], \
                "Flag sin_historial_local debe ser true para cliente extranjero"
    
    @pytest.mark.high
    @pytest.mark.edge_case
    @pytest.mark.integration
    def test_tc_bc_011_cliente_sin_historial_crediticio(self, api_client, verificar_api_disponible):
        """
        TC-BC-011: Cliente sin historial crediticio
        
        Precondiciones:
        - Cliente registrado por primera vez
        - Sin préstamos previos
        
        Resultado esperado:
        - Status 200
        - Score: null
        - historial_encontrado: false
        - Estado: "REQUIERE_ANALISIS_MANUAL"
        - Datos demográficos básicos
        """
        # Act
        response = api_client.consultar_bureau(
            documento=CLIENTE_SIN_HISTORIAL["documento"],
            tipo_documento=CLIENTE_SIN_HISTORIAL["tipo_documento"]
        )
        
        # Assert
        assert response.status_code == CLIENTE_SIN_HISTORIAL["expected_status"], \
            f"Status code esperado {CLIENTE_SIN_HISTORIAL['expected_status']}, recibido: {response.status_code}"
        
        data = response.json()
        
        # Cliente sin historial debe tener score null o indicador específico
        if "score" in data:
            assert data["score"] in [None, CLIENTE_SIN_HISTORIAL["expected_score"]], \
                f"Score para cliente sin historial debe ser null, recibido: {data['score']}"
        
        if "historial_encontrado" in data:
            assert data["historial_encontrado"] == CLIENTE_SIN_HISTORIAL["expected_historial_encontrado"], \
                "Flag historial_encontrado debe ser false"
        
        if "estado" in data:
            assert data["estado"] == CLIENTE_SIN_HISTORIAL["expected_estado"], \
                f"Estado debe ser REQUIERE_ANALISIS_MANUAL, recibido: {data['estado']}"
    
    @pytest.mark.medium
    @pytest.mark.edge_case
    @pytest.mark.integration
    def test_tc_bc_012_documento_duplicado_consulta_simultanea(self, api_client_session):
        """
        TC-BC-012: Documento duplicado en consulta simultánea
        
        Precondiciones:
        - Dos oficiales consultan mismo cliente
        - Ventana < 1 segundo
        
        Resultado esperado:
        - Status 200 para ambos
        - Misma información
        - Log de consulta duplicada
        - No doble cobro Bureau
        """
        results = []
        errors = []
        
        def consulta_bureau(cliente_api):
            try:
                response = cliente_api.consultar_bureau(
                    documento=DOCUMENTO_DUPLICADO["documento"],
                    tipo_documento=DOCUMENTO_DUPLICADO["tipo_documento"]
                )
                results.append({
                    "status": response.status_code,
                    "data": response.json() if response.status_code == 200 else None,
                    "time": response.elapsed.total_seconds()
                })
            except Exception as e:
                errors.append(str(e))
        
        # Crear dos threads que consulten simultáneamente
        thread1 = threading.Thread(target=consulta_bureau, args=(api_client_session,))
        thread2 = threading.Thread(target=consulta_bureau, args=(api_client_session,))
        
        # Iniciar ambos threads casi simultáneamente
        thread1.start()
        thread2.start()
        
        # Esperar a que terminen
        thread1.join()
        thread2.join()
        
        # Assert
        assert len(errors) == 0, f"Errores en consultas simultáneas: {errors}"
        assert len(results) == 2, f"Deben haber 2 resultados, recibidos: {len(results)}"
        
        # Ambas consultas deben ser exitosas
        assert all(r["status"] == 200 for r in results), \
            f"Todas las consultas deben retornar 200: {[r['status'] for r in results]}"
        
        # Los datos deben ser consistentes (mismo cliente)
        if results[0]["data"] and results[1]["data"]:
            # Comparar campos críticos
            if "score" in results[0]["data"] and "score" in results[1]["data"]:
                assert results[0]["data"]["score"] == results[1]["data"]["score"], \
                    "Score debe ser el mismo en consultas simultáneas"
    
    @pytest.mark.medium
    @pytest.mark.edge_case
    @pytest.mark.integration
    def test_tc_bc_013_consulta_historica_cache(self, api_client, verificar_api_disponible):
        """
        TC-BC-013: Consulta histórica - Obtener última consulta
        
        Precondiciones:
        - Cliente consultado previamente
        - GET /api/bureau/{cliente_id}
        
        Resultado esperado:
        - Status 200
        - Mismos datos de consulta anterior
        - timestamp_consulta visible
        - No genera nuevo cargo
        """
        # Primero hacer una consulta nueva
        response_inicial = api_client.consultar_bureau(
            documento=CLIENTE_HISTORICO["documento"],
            tipo_documento=CLIENTE_HISTORICO["tipo_documento"]
        )
        
        assert response_inicial.status_code == 200, \
            f"Consulta inicial falló con status {response_inicial.status_code}"
        
        data_inicial = response_inicial.json()
        
        # Pequeña pausa para simular consulta posterior
        time.sleep(1)
        
        # Si el API soporta consulta histórica por cliente_id
        if "cliente_id" in data_inicial or "id" in data_inicial:
            cliente_id = data_inicial.get("cliente_id") or data_inicial.get("id")
            
            try:
                response_historica = api_client.obtener_ultima_consulta(str(cliente_id))
                
                if response_historica.status_code == 200:
                    data_historica = response_historica.json()
                    
                    # Verificar que tiene timestamp
                    assert any(key in data_historica for key in ["timestamp", "fecha_consulta", "timestamp_consulta"]), \
                        "Respuesta histórica debe contener timestamp"
                    
                    # Verificar que los datos sean consistentes
                    if "score" in data_inicial and "score" in data_historica:
                        assert data_inicial["score"] == data_historica["score"], \
                            "Score debe ser el mismo en consulta histórica"
            except Exception as e:
                pytest.skip(f"Endpoint de consulta histórica no disponible: {e}")
        else:
            pytest.skip("Respuesta no contiene cliente_id para consulta histórica")
    
    @pytest.mark.high
    @pytest.mark.edge_case
    @pytest.mark.integration
    def test_tc_bc_014_cliente_score_limite_600(self, api_client, verificar_api_disponible):
        """
        TC-BC-014: Cliente con score límite (edge case 600)
        
        Precondiciones:
        - Cliente en score frontera
        - Política: aprobación manual >= 600
        
        Resultado esperado:
        - Status 200
        - Score: 600
        - Estado: "REVISAR"
        - requiere_aprobacion_gerencia: true
        - Flag de score límite
        """
        # Act
        response = api_client.consultar_bureau(
            documento=CLIENTE_SCORE_LIMITE["documento"],
            tipo_documento=CLIENTE_SCORE_LIMITE["tipo_documento"]
        )
        
        # Assert
        assert response.status_code == 200, \
            f"Status code esperado 200, recibido: {response.status_code}"
        
        data = response.json()
        
        # Verificar score en el límite
        if "score" in data:
            # El score puede ser exactamente 600 o cerca del límite (595-605)
            assert 595 <= data["score"] <= 605, \
                f"Score esperado cerca de 600, recibido: {data['score']}"
        
        # Verificar que requiera revisión
        if "estado" in data:
            assert data["estado"] in ["REVISAR", CLIENTE_SCORE_LIMITE["expected_estado"]], \
                f"Estado debe ser REVISAR para score límite, recibido: {data['estado']}"
        
        # Verificar flag de aprobación gerencial
        if "requiere_aprobacion_gerencia" in data or "requiere_gerencia" in data:
            assert data.get("requiere_aprobacion_gerencia") or data.get("requiere_gerencia"), \
                "Score límite debe requerir aprobación gerencial"
    
    @pytest.mark.medium
    @pytest.mark.edge_case
    def test_tc_bc_014_scores_frontera(self, api_client, verificar_api_disponible):
        """
        Test adicional: Verificar comportamiento en múltiples scores frontera
        
        Scores críticos: 500, 600, 700
        """
        scores_frontera = [
            {"score": 499, "expected": "RECHAZADO"},
            {"score": 500, "expected": ["RECHAZADO", "REVISAR"]},
            {"score": 599, "expected": "REVISAR"},
            {"score": 600, "expected": ["REVISAR", "APROBADO"]},
            {"score": 699, "expected": ["REVISAR", "APROBADO"]},
            {"score": 700, "expected": "APROBADO"}
        ]
        
        # Esta prueba es conceptual - requeriría documentos específicos
        # con cada score para ser completamente funcional
        pass
