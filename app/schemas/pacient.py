from pydantic import BaseModel, Field
from typing import Optional

class PacientBase(BaseModel):
    cedula: str = Field(..., max_length=20)
    name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    age: int
    birth_date: str = Field(..., max_length=20)
    gender: str = Field(..., max_length=20)
    phone: str = Field(..., max_length=20)

class PacientCreate(PacientBase):
    pass

class PacientRead(PacientBase):
    id: int

    class Config:
        orm_mode = True

class PacientUpdate(BaseModel):
    cedula: Optional[str] = Field(None, max_length=20)
    name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    age: Optional[int] = None
    birth_date: Optional[str] = Field(None, max_length=20)
    gender: Optional[str] = Field(None, max_length=20)
    phone: Optional[str] = Field(None, max_length=20)
