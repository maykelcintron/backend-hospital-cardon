from sqlmodel import SQLModel, Field
from typing import Optional

class Pacient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cedula: str = Field(unique=True, index=True)
    name: str
    last_name: str
    age: int
    birth_date: str
    gender: str
    phone: str
