"""Schemas compartilhados da aplicação."""

from pydantic import BaseModel, EmailStr, constr
from datetime import datetime


class UserCreate(BaseModel):
    """Schema para criação de usuário."""
    nome: constr(min_length=3, max_length=100)
    email: EmailStr
    senha: constr(min_length=8, max_length=72)

    class Config:
        from_attributes = True


# pylint: disable=too-few-public-methods
class UserOut(BaseModel):
    """Schema para saída de usuário."""
    id: int
    nome: str
    email: EmailStr
    data_cadastro: datetime

    class Config:
        from_attributes = True


# pylint: disable=too-few-public-methods
class UserUpdate(BaseModel):
    """Schema para atualização de usuário."""
    nome: constr(min_length=3, max_length=100) = None
    email: EmailStr = None
    senha: constr(min_length=8, max_length=72) = None
