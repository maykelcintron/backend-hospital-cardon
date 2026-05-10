from pydantic import BaseModel, Field
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., min_length=1, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=72)  # Limitar a 72 caracteres

class UserRead(UserBase):
    id: int

class UserLogin(BaseModel):
    email: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1, max_length=72)