from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from routers.jwt_man import token_router
from routers.usuarios import usuarios_router
from routers.categorias import Categoria_router
from routers.inscripciones import inscripciones_router
from routers.eventos import eventos_router

from starlette.middleware.cors import CORSMiddleware
app = FastAPI()
origins = [
    "http://127.0.0.1:5501",  # Origen de tu HTML
    "http://localhost:5501",  # Origen de tu HTML (alternativo)
    "http://127.0.0.1:5500",  # Origen de tu HTML
    "http://localhost:5500",  # Origen de tu HTML (alternativo)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)
app.title = "SISTEMA DE GESTIÓN DE EVENTOS"
app.version = "0.0.1"

app.include_router(token_router)
app.include_router(usuarios_router)
app.include_router(Categoria_router)
app.include_router(inscripciones_router)
app.include_router(eventos_router)

Base.metadata.create_all(bind=engine)

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>SISTEMA DE GESTIÓN DE EVENTOS</h1>')
