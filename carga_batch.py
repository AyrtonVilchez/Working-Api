import concurrent.futures
import time
from typing import List, Dict, Callable
import pandas as pd
from basic_request import APIClient

class BatchDataCarga:
    """
    Carga eficiente de datos de multiples Edpoints
    """

    def __init__(self, api_client: APIClient, max_workers: int =5):
        self.client = api_client
        self.max_workers = max_workers
    
    def carga_paralela(self, endpoints: List[str]):
        """
        Carg data de multiples endpoint en paralelo

        Arg:
            endpoints: Lista de API endpoints
        
        Returns:
            Diccionario con las respuestas de cada endpoint
        """
        results = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Enviar todas las tareas
            future_to_endpoint = {
                executor.submit(self.client.get, endpoint): endpoint
                for endpoint in endpoints
            }

            # Almacenar los datos completados
            for future in concurrent.futures.as_completed(future_to_endpoint):
                endpoint = future_to_endpoint[future]
                try:
                    data = future.result()
                    results[endpoint] = data
                    print(f"Carga exitosa de {endpoint}")
                except Exception as e:
                    print(f"Error al obtener datos de {endpoint}: {str(e)}")
                    results[endpoint] = None

        return results
    
    def carga_con_transformaciones(self, endpoints: List[str], transform_func: Callable):
        """
        Coleccionar la data y transformala en un DataFrame

        Args:
            endpoints: Lista de API endpoints
            transform_func: Funcion de transformacion de raw_data

        Returns:
            DataFrame con la data transformada
        """
        raw_data = self.carga_paralela(endpoints)
        
        data_transformada = []
        for endpoint, data in raw_data.items():
            if data :
                transformada = transform_func(data, endpoint)
                data_transformada.extend(transformada)
        
        return pd.DataFrame(data_transformada)
    


