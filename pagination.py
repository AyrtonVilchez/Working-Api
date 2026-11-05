import time
from basic_request import APIClient
from typing import Generator, List, Dict, Optional

class PaginadaAPIClient(APIClient):
    """
    Version extendida de APICliente para soportar paginacion
    """

    def fetch_all_pages(self, endpoint: str, page_size: int = 100,
                        max_pages: Optional[int] = None):
        """
        Capturamos todas las paginas de un endpoint paginado

        Args:
            endpoint: API endpoint
            page_size: Numero de items por pagina
            max_pages: Numero maximo de paginas a capturar
        Returns:
            Lista de todos los items de todas las paginas
        """
        all_items = []
        page = 1

        while True:
            # revisa si hay un maximo de paginas
            if max_pages and page > max_pages:
                break

            # obtiene los items de la pagina actual
            params ={'page': page, 'per_page': page_size}
            response = self.get(endpoint, params=params)

            # revisar si la solicitud esta vacio o ha llegado al final
            if not response or len(response) == 0:
                break
            
            all_items.extend(response)
            print(f"Pagina cargada {page} con {len(response)} elementos")

            # revisa si hay menos que el page_size (last_page)
            if len(response) < page_size:
                break

            page += 1
            time.sleep(0.1)

        return all_items
        
# Example
# En la PokeAPI no existe paginacion para el ejemplo de llevar lista de pokemones
    