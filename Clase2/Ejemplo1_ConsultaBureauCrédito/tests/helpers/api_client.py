"""
Helper para cliente HTTP del API
"""
import os
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class BureauAPIClient:
    """Cliente HTTP para interactuar con el API de Bureau de Crédito"""
    
    def __init__(self, base_url: str = None, timeout: int = None):
        self.base_url = base_url or os.getenv("API_BASE_URL", "http://localhost:8000")
        self.timeout = timeout or int(os.getenv("API_TIMEOUT", "5"))
        self.session = requests.Session()
    
    def consultar_bureau(self, documento: str, tipo_documento: str = "CC") -> requests.Response:
        """
        Consultar Bureau de Crédito
        
        Args:
            documento: Número de documento
            tipo_documento: Tipo de documento (CC, CE, NIT, PAS)
            
        Returns:
            Response del API
        """
        url = f"{self.base_url}/api/bureau/consultar"
        payload = {
            "documento": documento,
            "tipo_documento": tipo_documento
        }
        return self.session.post(url, json=payload, timeout=self.timeout)
    
    def obtener_ultima_consulta(self, cliente_id: str) -> requests.Response:
        """
        Obtener última consulta de Bureau
        
        Args:
            cliente_id: ID del cliente
            
        Returns:
            Response del API
        """
        url = f"{self.base_url}/api/bureau/{cliente_id}"
        return self.session.get(url, timeout=self.timeout)
    
    def solicitar_prestamo(self, payload: Dict[str, Any]) -> requests.Response:
        """
        Solicitar préstamo
        
        Args:
            payload: Datos de la solicitud
            
        Returns:
            Response del API
        """
        url = f"{self.base_url}/api/prestamos/solicitar"
        return self.session.post(url, json=payload, timeout=self.timeout)
    
    def obtener_estado_prestamo(self, prestamo_id: str) -> requests.Response:
        """
        Obtener estado del préstamo
        
        Args:
            prestamo_id: ID del préstamo
            
        Returns:
            Response del API
        """
        url = f"{self.base_url}/api/prestamos/{prestamo_id}/estado"
        return self.session.get(url, timeout=self.timeout)
    
    def health_check(self) -> requests.Response:
        """Verificar estado del API"""
        url = f"{self.base_url}/health"
        return self.session.get(url, timeout=2)
    
    def close(self):
        """Cerrar sesión HTTP"""
        self.session.close()
