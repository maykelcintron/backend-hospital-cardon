from typing import List

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.core.db import SessionDep
from app.models.pacient import Pacient
from app.schemas.pacient import PacientCreate, PacientRead, PacientUpdate

router = APIRouter(prefix="/pacients", tags=["pacients"])

@router.post("/", response_model=PacientRead)
async def create_pacient(data: PacientCreate, session: SessionDep):
    existing = session.exec(select(Pacient).where(Pacient.cedula == data.cedula)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un paciente con esa cédula")

    pacient = Pacient(**data.dict())
    session.add(pacient)
    session.commit()
    session.refresh(pacient)
    return pacient

@router.get("/", response_model=List[PacientRead])
async def list_pacients(session: SessionDep):
    pacients = session.exec(select(Pacient)).all()
    return pacients

@router.get("/{pacient_id}", response_model=PacientRead)
async def get_pacient(pacient_id: int, session: SessionDep):
    pacient = session.get(Pacient, pacient_id)
    if not pacient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return pacient

@router.put("/{pacient_id}", response_model=PacientRead)
async def update_pacient(pacient_id: int, data: PacientUpdate, session: SessionDep):
    pacient = session.get(Pacient, pacient_id)
    if not pacient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    if data.cedula and data.cedula != pacient.cedula:
        exists = session.exec(select(Pacient).where(Pacient.cedula == data.cedula)).first()
        if exists:
            raise HTTPException(status_code=400, detail="Otra persona ya usa esa cédula")

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(pacient, key, value)

    session.add(pacient)
    session.commit()
    session.refresh(pacient)
    return pacient

@router.delete("/{pacient_id}", status_code=204)
async def delete_pacient(pacient_id: int, session: SessionDep):
    pacient = session.get(Pacient, pacient_id)
    if not pacient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    session.delete(pacient)
    session.commit()
    return None
