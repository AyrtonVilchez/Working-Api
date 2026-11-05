import requests
import json
from typing import Dict, Optional, List

class APIClient:
    """
    Es un robusto Cliente de API con manejo de errores
    """
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
    
    def _build_url(self, endpoint: str):
        """Constructor de la url completa basado en la url base y un endpoint"""
        return f"{self.base_url}/{endpoint.lstrip('/')}"
    
    def get(self, endpoint: str, params: Optional[Dict] = None):
        """
        Hacemos GET request a la API del endpoint

        Args:
            endpoint (str): endpoint de la API
            params: los parametros de consulta
        
        Returns:
            dict: la data como un diccionario
        """
        url = self._build_url(endpoint)
        try:
            response = self.session.get(
                url,
                params = params,
                timeout = self.timeout
            )
            #Previene errores en status code
            response.raise_for_status() 
            return response.json()
        except requests.exceptions.Timeout:
            print(f"Se acabo el tiempo para {url}")
            raise
        except requests.exceptions.ConnectionError:
            print(f"Error de conexion para {url}")
            raise
        except requests.exceptions.HTTPError as e:
            print(f"Error en el status code {e.response.status_code} para {url}")
            raise
        except json.JSONDecodeError:
            print(f"JSON invalido para {url}")
            print(f"{response.text}")
            raise
        
# Example
#poke_client = APIClient('https://pokeapi.co/api/v2')

#params ={
#     'offset': 0,
#     'limit': 20
# }
# GET request
# poke_form = poke_client.get('pokemon-form', params = params)
# poke_names = poke_form.get('results', {})
# print(f"Se cargaron {len(poke_names)} pokemones")

