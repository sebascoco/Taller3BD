from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import os
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

client = MongoClient(os.environ["MONGO_URI"])
db_propia = client["ISIS2304C29202610"]  # escritura: comentarios y eventos
db_bares  = client["ISIS2304"]           # lectura: bares y bebedores

@app.get("/")
def inicio():
    return {"estado": "API funcionando correctamente"}

@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: int):
    comentarios = list(db_propia["comentarios_bares"].find({"bar_id": bar_id}, {"_id": 0}))
    return comentarios

@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha'] = datetime.now().isoformat()
    datos['date'] = datetime.utcnow()
    db_propia["comentarios_bares"].insert_one(datos)
    return {'mensaje': 'Comentario guardado'}

@app.get('/bares/{bar_id}/eventos')
def get_eventos(bar_id: int):
    eventos = list(db_propia["eventos"].find({"bar_id": bar_id}, {"_id": 0}))
    return eventos

@app.post('/bares/{bar_id}/eventos')
def post_evento(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha_creacion'] = datetime.now().isoformat()
    db_propia["eventos"].insert_one(datos)
    return {'mensaje': 'Evento guardado'}

@app.get('/bares/{bar_id}')
def get_bares(bar_id: int):
    bar = db_bares["Bares"].find_one({"_id": bar_id}, {"_id": 0})
    return bar