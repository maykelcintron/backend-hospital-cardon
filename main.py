from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router import auth
from app.router import pacients
from app.router import exams
from app.core.db import create_all_tables, engine
from sqlmodel import Session, select
from app.models.exam import ExamType

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
    initialize_exam_types()

def initialize_exam_types():
    exam_types = [
        "Seriologia",
        "Quimica Sanguinea",
        "Estudios de Coagulacion",
        "Analisis de Heces",
        "Analisis de Orina",
        "Hematologia"
    ]
    with Session(engine) as session:
        for name in exam_types:
            existing = session.exec(select(ExamType).where(ExamType.name == name)).first()
            if not existing:
                session.add(ExamType(name=name))
        session.commit()

app.include_router(auth.router, prefix="/api/v1")
app.include_router(pacients.router, prefix="/api/v1")
app.include_router(exams.router, prefix="/api/v1")

@app.get("/")
async def read_root():
    return {"Hello": "World"}

