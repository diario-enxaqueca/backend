from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, constr


# pylint: disable=too-few-public-methods
class UserCreate(BaseModel):
    nome: constr(min_length=3, max_length=100)
    email: EmailStr
    senha: constr(min_length=8, max_length=72)

    class Config:
        from_attributes = True


# pylint: disable=too-few-public-methods
class UserOut(BaseModel):
    id: int
    nome: str
    email: EmailStr
    data_cadastro: datetime

    class Config:
        from_attributes = True


# pylint: disable=too-few-public-methods
class UserUpdate(BaseModel):
    nome: Optional[constr(min_length=3, max_length=100)] = None
    email: Optional[EmailStr] = None
    senha: Optional[constr(min_length=8, max_length=72)] = None
