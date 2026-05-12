from sqlmodel import create_engine, SQLModel, Session
from dotenv import load_dotenv
from fastapi import Depends
from typing import Annotated
import os

from app.models.user import User  # Importar el modelo
from app.models.pacient import Pacient
from app.models.exam import Exam, ExamType

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("LA URL DE LA BASE DE DATOS NO ESTÁ CONFIGURADA EN EL ARCHIVO .env")

engine = create_engine(DATABASE_URL)

def create_all_tables():
    SQLModel.metadata.create_all(engine)
    print("Tablas creadas exitosamente")

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]