from pydantic import BaseModel, EmailStr, constr
from datetime import datetime


class UserCreate(BaseModel):
    nome: constr(min_length=3, max_length=100)
    email: EmailStr
    senha: constr(min_length=8, max_length=72)

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: int
    nome: str
    email: EmailStr
    data_cadastro: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
