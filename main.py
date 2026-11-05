from carga_batch import BatchDataCarga
from basic_request import APIClient
import pandas as pd
from typing import Dict
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

endpoints=[]

def data_tranformada_pokemon(data: Dict, source: str):
    """
        Transformar la data de un pokemon en un formato standar
    """
    if isinstance(data, dict):
        return [
            {
                "id": data.get("id"),
                "nombre": data.get("name"),
                "altura": data.get("height"),
                "peso": data.get("weight"),
                "fec_actualizacion": pd.Timestamp.now()
            }
            ]
    return []


def get_endpoints(poke_client: APIClient, url_base, offset = 0):
    params = { 'offset': offset, 'limit':20} if offset else {}

    #GET request
    poke_form = poke_client.get(url_base, params = params)
    poke_names = poke_form.get('results', {})
    
    if poke_names:
        for pokemon in poke_names:
            endpoints.append(f"/{pokemon['name']}")

    return endpoints        

 

# Gnerar endpoints
poke_client = APIClient('https://pokeapi.co/api/v2')
url_base= 'pokemon-form'
offset = 0
while offset <= 1560:
    get_endpoints(poke_client, url_base, offset)
    offset += 20

# #Crear Colector
api_cliente = APIClient("https://pokeapi.co/api/v2/pokemon")
colector = BatchDataCarga(api_cliente, max_workers=3)

# # Cargar de multiples endpoints
# endpoints =['/bulbasaur', '/ivysaur','/venusaur','/charmander', '/charmeleon']
# #all_data = colector.carga_paralela(endpoints)

# # Coleccionar y trasformar data de pokemon
# #pokemon_endpoints = ['/bulbasaur']
pokemon_df = colector.carga_con_transformaciones(endpoints, data_tranformada_pokemon)
print(pokemon_df.head())

# Llevando a un dataFrame de PySpark
# Creacion del schema
schema = StructType([
            StructField('id', IntegerType(), True), 
            StructField('name', StringType(), True),
            StructField('height', IntegerType(), True),
            StructField('weight', IntegerType(), True)
        ])

df_pokemon = spark.createDataFrame(pokemon_df, schema = schema)

# Se lleva el dataFrame a una tabla en el ambiente bronze
df_pokemon.write.mode("overwrite").saveAsTable("academy.bronze.pokemon_info")
