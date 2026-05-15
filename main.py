from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# os.environ para despliegue. Descomente cuando ya probó todo local.
client = MongoClient(os.environ["MONGO_URI"])
# TODO: conectarse al cluster Admonsis  
# client = MongoClient("mongodb://ISIS2304C29202610:OE6wZSWPzb54@157.253.236.88:8087")

# client = MongoClient("mongodb://ISIS2304C29202610:OE6wZSWPzb54@157.253.236.88:8087")
# TODO: conectarse a la base de datos Admonsis  
# db = client["ISIS*******"]
db = client["ISIS2304"]


@app.get("/")
def inicio():
    return {"estado": "API funcionando correctamente"}

@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: int):
    comentarios = list(db["comentarios_bares"].find({"bar_id": bar_id}, {"_id": 0}))
    return comentarios

@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha']  = datetime.now().isoformat()
    db["comentarios_bares"].insert_one(datos)
    return {'mensaje': 'Comentario guardado'}

# TODO: implementar GET /bares/{bar_id}/eventos
# Debe retornar todos los eventos del bar desde la colección 'eventos'
@app.get('/bares/{bar_id}/eventos')
def get_eventos(bar_id: int):
    eventos = list(db["eventos"].find({"bar_id": bar_id}, {"_id": 0}))
    return eventos

# TODO: implementar POST /bares/{bar_id}/eventos  
# Debe insertar el evento en la colección 'eventos'
# Recuerde agregar bar_id y fecha_creacion al documento antes de insertar
@app.post('/bares/{bar_id}/eventos')
def post_evento(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha_creacion'] = datetime.now().isoformat()
    db["eventos"].insert_one(datos)
    return {'mensaje': 'Evento guardado'}

@app.get('/bares/{bar_id}')
def get_bares(bar_id: int):
    bar = db["Bares"].find_one({"_id": bar_id}, {"_id": 0})
    return bar

@app.get('/test')
def test_conexion():
    try:
        colecciones = db.list_collection_names()
        bar = db["Bares"].find_one({"_id": 58}, {"_id": 0})
        return {
            "colecciones": colecciones,
            "bar_58": bar
        }
    except Exception as e:
        return {"error": str(e)}