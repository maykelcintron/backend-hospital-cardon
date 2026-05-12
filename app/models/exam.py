from sqlmodel import SQLModel, Field
from typing import Optional

class ExamType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)

class Exam(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pacient_id: int = Field(foreign_key="pacient.id")
    exam_type_id: int = Field(foreign_key="examtype.id")
    exam_date: str