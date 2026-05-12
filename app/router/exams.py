from typing import List
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.core.db import SessionDep
from app.models.exam import Exam, ExamType
from app.models.pacient import Pacient
from app.schemas.exam import ExamCreate, ExamRead, ExamCalculateRequest, ExamResult, ExamTypeRead

router = APIRouter(prefix="/exams", tags=["exams"])

# Endpoint para crear examen
@router.post("/", response_model=ExamRead)
async def create_exam(data: ExamCreate, session: SessionDep):
    # Verificar que el paciente existe
    pacient = session.get(Pacient, data.pacient_id)
    if not pacient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    # Verificar que el tipo de examen existe
    exam_type = session.get(ExamType, data.exam_type_id)
    if not exam_type:
        raise HTTPException(status_code=404, detail="Tipo de examen no encontrado")

    exam = Exam(**data.dict())
    session.add(exam)
    session.commit()
    session.refresh(exam)
    return exam

# Endpoint para listar exámenes
@router.get("/", response_model=List[ExamRead])
async def list_exams(session: SessionDep):
    exams = session.exec(select(Exam)).all()
    return exams

# Endpoint para obtener un examen
@router.get("/{exam_id}", response_model=ExamRead)
async def get_exam(exam_id: int, session: SessionDep):
    exam = session.get(Exam, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Examen no encontrado")
    return exam

# Endpoint para calcular resultados
@router.post("/calculate", response_model=ExamResult)
async def calculate_exam_results(data: ExamCalculateRequest, session: SessionDep):
    exam = session.get(Exam, data.exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Examen no encontrado")

    exam_type = session.get(ExamType, exam.exam_type_id)
    results = {}

    if exam_type.name == "Quimica Sanguinea":
        results = calculate_quimica_sanguinea(data.parameters)
    elif exam_type.name == "Seriologia":
        results = calculate_seriologia(data.parameters)
    elif exam_type.name == "Estudios de Coagulacion":
        results = calculate_coagulacion(data.parameters)
    else:
        # Para otros tipos, devolver los parámetros tal cual
        results = data.parameters

    return ExamResult(exam_id=data.exam_id, results=results)

def calculate_quimica_sanguinea(params: dict) -> dict:
    ranges = {
        "Glucosa Oxidasa": (70, 105),
        "bun": (7, 18),
        "Acido Urico": (2.5, 7.7),
        "Colesterol total": (0, 200),
        "Colesterol HDL": (30, 85),
        "Colesterol LDH": (0, 150),
        "Trigliceridos": (44, 148),
        "Proteinas totales": (6.0, 8.2),
        "Albumina": (3.5, 5.3),
        "Globulina": (2.5, 3.5),
        "Relacion A/G": (1.0, 1.8),
        "Calcio Arsenato": (8.5, 10.4),
        "Fosforo": (2.5, 4.8),
        "Magnesio": (1.6, 3.0),
        "gpt / alt": (4, 36),
        "got / ast": (5, 34),
        "Bilirrubina total": (0.2, 1.2),
        "Bilirrubina Directa": (0.0, 0.2),
        "Bilirrubina Indirecta": (0.0, 1.0),
        "Fosfatasa Alcalina": (25, 180),
        "Lactico Deshidrogenasa": (80, 285),
        "Gamma GT": (6, 37),
        "Amilasa": (25, 125),
        "Creatinkinasa": (0, 160),
        "Hierro total": (60, 150),
        "CK - MB": (0, 24),
        "PCR": (0, 0.3),
        "Creatinina": (0.4, 1.4)
    }
    results = {}
    for param, value in params.items():
        if param in ranges:
            min_val, max_val = ranges[param]
            status = "Normal" if min_val <= value <= max_val else "Anormal"
            results[param] = {"value": value, "range": f"{min_val}-{max_val}", "status": status}
        else:
            results[param] = {"value": value, "status": "Sin rango definido"}
    return results

def calculate_seriologia(params: dict) -> dict:
    # Para Seriología, solo devolver los valores, ya que no se especifican rangos
    return {k: {"value": v} for k, v in params.items()}

def calculate_coagulacion(params: dict) -> dict:
    # Para Coagulación, devolver valores, algunos con cálculos simples si aplica
    results = {}
    for k, v in params.items():
        if "Tiempo de protombinica" in k or "Tiempo parcial de tromboplasmina" in k:
            # Asumir que son tiempos, devolver tal cual
            results[k] = {"value": v}
        elif "Actividad protombinica" in k:
            results[k] = {"value": v}
        elif "Diferencia" in k:
            results[k] = {"value": v, "note": "V.N +/-6"}
        elif "Razon" in k:
            results[k] = {"value": v, "note": "0.8 a 1.2"}
        elif "INR" in k:
            results[k] = {"value": v}
        elif "Fibronogeno" in k:
            results[k] = {"value": v, "note": "200-400 mg/%"}
        else:
            results[k] = {"value": v}
    return results

# Endpoint para listar tipos de examen
@router.get("/types", response_model=List[ExamTypeRead])
async def list_exam_types(session: SessionDep):
    types = session.exec(select(ExamType)).all()
    return types