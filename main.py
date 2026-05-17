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
    allow_headers=["*"],
)

# En Render debes definir MONGO_URI en Environment Variables.
# Value: mongodb://tuusuario:tucontrasena@157.253.236.88:8087  (según guía)
MONGO_URI = os.environ.get("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError("Falta la variable de entorno MONGO_URI")

client = MongoClient(MONGO_URI)

# Base de datos de tu usuario (en tu caso coincide con la captura)
db = client["ISIS2304D26202610"]

API_PREFIX = "/api"

@app.get("/")
def inicio():
    return {"estado": "API funcionando correctamente"}


# GET /api/bares/{bar_id}/comentarios
@app.get(f"{API_PREFIX}/bares/{{bar_id}}/comentarios")
def get_comentarios(bar_id: int):
    comentarios = list(
        db["comentarios"].find({"bar_id": bar_id}, {"_id": 0})
    )
    return comentarios


# POST /api/bares/{bar_id}/comentarios
@app.post(f"{API_PREFIX}/bares/{{bar_id}}/comentarios")
def post_comentario(bar_id: int, datos: dict):
    datos["bar_id"] = bar_id
    datos["fecha"] = datetime.now().isoformat()

    db["comentarios"].insert_one(datos)
    return {"mensaje": "Comentario guardado"}


# GET /api/bares/{bar_id}/eventos
@app.get(f"{API_PREFIX}/bares/{{bar_id}}/eventos")
def get_eventos(bar_id: int):
    eventos = list(
        db["eventos"].find({"bar_id": bar_id}, {"_id": 0})
    )
    return eventos


# POST /api/bares/{bar_id}/eventos
@app.post(f"{API_PREFIX}/bares/{{bar_id}}/eventos")
def post_evento(bar_id: int, datos: dict):
    datos["bar_id"] = bar_id
    datos["fecha_creacion"] = datetime.now().isoformat()

    db["eventos"].insert_one(datos)
    return {"mensaje": "Evento creado"}
