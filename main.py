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

# conexión Mongo (usar variable de entorno en Render)
MONGO_URI = os.environ.get("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError("Falta la variable MONGO_URI")

client = MongoClient(MONGO_URI)

# tu base de datos
db = client["ISIS2304D26202610"]


@app.get("/")
def inicio():
    return {"estado": "API funcionando correctamente"}


# ✅ GET comentarios
@app.get("/bares/{bar_id}/comentarios")
def get_comentarios(bar_id: int):
    comentarios = list(
        db["comentarios"].find({"bar_id": bar_id}, {"_id": 0})
    )
    return comentarios


# ✅ POST comentarios
@app.post("/bares/{bar_id}/comentarios")
def post_comentario(bar_id: int, datos: dict):
    datos["bar_id"] = bar_id
    datos["fecha"] = datetime.now().isoformat()

    db["comentarios"].insert_one(datos)
    return {"mensaje": "Comentario guardado"}


# ✅ GET eventos
@app.get("/bares/{bar_id}/eventos")
def get_eventos(bar_id: int):
    eventos = list(
        db["eventos"].find({"bar_id": bar_id}, {"_id": 0})
    )
    return eventos


# ✅ POST eventos
@app.post("/bares/{bar_id}/eventos")
def post_evento(bar_id: int, datos: dict):
    datos["bar_id"] = bar_id
    datos["fecha_creacion"] = datetime.now().isoformat()

    db["eventos"].insert_one(datos)
    return {"mensaje": "Evento creado"}
``
