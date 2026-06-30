import uvicorn
from typing import Union, Optional
from fastapi import FastAPI
from fastapi import HTTPException
import psycopg2
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
import base64
import requests
import  dbConfig 
import serviceMongoOrion
import urbanMovility
import serviceOrionSettings
import os
import psutil

MONGO_URI = "mongodb://localhost:27017"
MONGO_DB = "mi_base"

app = FastAPI()
# Lista de orígenes permitidos
origins = [
    "http://localhost:5173",
    "http://locahost"  # Vite dev server
    # Puedes agregar más orígenes si los necesitas
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/db-status-postgis")
def db_status():
    try:
        conn = psycopg2.connect(**dbConfig.DB_POSTGIS_CONFIG)
        conn.close()
        return {"status": "PostGIS is connected"}
    except Exception as e:
        return {"status": f"Failed to connect: {e}"}
    
    
@app.get("/db-status-mongo")
async def db_status():
    try:
        print('Conectando a Mongo')
        client = MongoClient(dbConfig.DB_MONGO_CONFIG)
        databases = client.list_database_names()
        for db in databases: 
            if db.startswith("orion"):
                return f"Mongo is connected - {db.upper()} found"
    except Exception as e:
        return {"status": f"Failed to connect: {e}"}
    

@app.get("/getOrionServices")
def getOrionServices():
    print(f"Obteniendo servicios Orion")
    results = serviceMongoOrion.getOrionServices()
    return results

@app.get("/getOrionServicesWithServicePath/{service}")
def getOrionServicesWithServicePath(servicie: Optional[str] = ''):
    print(f"getOrionServicesWithServicePath")
    if servicie=='':
        return []
    results=serviceMongoOrion.getOrionServicesWithServicePath(servicie)
    return results



@app.post("/setOrionService/{service}")
def setOrionService(service):
    print(f"Creacion servicio {service} en orion")
    if service==[]:
        raise HTTPException(status_code=404, detail="No se encontraron resultados de subservicios de Orion") 
    results = serviceMongoOrion.setOrionService(service)
    if results:
        return results
    else:
        raise HTTPException(status_code=404, detail="No se creo el servicio {service}") 



@app.get("/getOrionServicesPath/")
@app.get("/getOrionServicesPath/{service}")
def getOrionServicesPath(service: Optional[str] = ''):
    print(f"Obteniendo servicios Orion")
    if service=='':
        return []
    results = serviceMongoOrion.getServiceServicePath(service)
    if results:
        return results
    else:
        raise HTTPException(status_code=404, detail="No se encontraron resultados de subservicios de Orion") 


@app.get("/busPositions/")
def BusPoitions():
    print(f"Obteniendo posiciones de urbanMovility")
    results = urbanMovility.getBusPositions()
    if results:
        return results
    else:
        raise HTTPException(status_code=404, detail="No se encontraron posiciones de urbanMovility")


# ORION WEB SETTINGS
@app.get("/getOrionWebSettings")
def getOrionWebSettings():
    print(f"Obteniendo configuracion web de orion")
    results = serviceOrionSettings.getOrionWebSettings()
    if results:
        return results
    else:
        raise HTTPException(status_code=404, detail="No se encontraron configuraciones web de Orion")

@app.get("/setOrionWebSettings/{data}")
def setOrionWebSettings(data: str):
    print(f"Obteniendo configuracion web de orion")
    results = serviceOrionSettings.setOrionWebSettings(data)
    if results:
        return results
    else:
        raise HTTPException(status_code=404, detail="No se encontraron configuraciones web de Orion")


# Endpoint para obtener el uso de CPU
def obtener_info_procesador():
    # 1. Contar núcleos totales (físicos + virtuales/hilos)
    # Si tu CPU tiene 4 núcleos y 8 hilos, esto devolverá 8.
    nucleos_totales = os.cpu_count() or 1
    nucleos_fisicos = psutil.cpu_count(logical=False)
    
    # 2. Obtener el porcentaje de uso actual de la CPU (promedio de todos los núcleos)
    # 'interval=None' lo hace instantáneo basándose en la última llamada
    uso_cpu_porcentaje = psutil.cpu_percent(interval=0.1)
    
    
    # 3. Contar cuántas instancias de SUMO se están ejecutando actualmente en el sistema
    sumo_activos = 0
    for proc in psutil.process_iter(['name']):
        try:
            # Buscamos procesos que se llamen 'sumo' o 'sumo-gui'
            if proc.info['name'] and 'sumo' in proc.info['name'].lower():
                sumo_activos += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return {
        "nucleos_totales": nucleos_totales,
        "nucleos_fisicos": nucleos_fisicos,
        "uso_cpu_actual_porcentaje": uso_cpu_porcentaje,
        "simulaciones_sumo_corriendo": sumo_activos,
        "nucleos_disponibles_estimados": max(0, nucleos_totales - sumo_activos)
    }

@app.get("/server-status/")
async def server_status():
    """Endpoint para monitorizar el servidor desde fuera"""
    return obtener_info_procesador()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)