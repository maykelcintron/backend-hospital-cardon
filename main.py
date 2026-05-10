from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router import auth
from app.core.db import create_all_tables

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir las fuentes especificadas (en producción, restringir esto)
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
    allow_credentials=True,  # Permitir el envío de cookies y credenciales
)

# Crear tablas al iniciar la aplicación
@app.on_event("startup")
def on_startup():
    create_all_tables()

app.include_router(auth.router, prefix="/api/v1")

@app.get("/")
async def read_root():
    return {"Hello": "World"}

