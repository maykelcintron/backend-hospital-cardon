from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class ExamTypeBase(BaseModel):
    name: str = Field(..., max_length=100)

class ExamTypeCreate(ExamTypeBase):
    pass

class ExamTypeRead(ExamTypeBase):
    id: int

    class Config:
        orm_mode = True

class ExamBase(BaseModel):
    pacient_id: int
    exam_type_id: int
    exam_date: str = Field(..., max_length=20)

class ExamCreate(ExamBase):
    pass

class ExamRead(ExamBase):
    id: int

    class Config:
        orm_mode = True

class ExamCalculateRequest(BaseModel):
    exam_id: int
    parameters: Dict[str, Any]  # Los parámetros específicos del examen

class ExamResult(BaseModel):
    exam_id: int
    results: Dict[str, Any]  # Los resultados calculados