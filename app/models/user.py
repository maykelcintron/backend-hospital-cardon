from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    password: str  # Deberías hashear la contraseña
    role: str 

# class Exams(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     pacient_id: int = Field(foreign_key="pacients.id")
#     exam_type: int = Field(foreign_key="exam_types.id")
#     exam_date: str
#     id_results: int = Field(foreign_key="results.id")

# class ExamTypes(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str

# class Results(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     pacient_id: int = Field(foreign_key="pacients.id")
#     exam_id: int = Field(foreign_key="exams.id")
#     result_data: str