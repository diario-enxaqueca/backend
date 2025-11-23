from datetime import datetime
from pydantic import BaseModel, Field, constr

# pylint: disable=too-few-public-methods

# --- SCHEMAS ---


class GatilhoCreate(BaseModel):
    nome: constr(strip_whitespace=True,
                 min_length=2, max_length=100) = Field(
                     ..., description="Nome do gatilho "
                     "(ex: Estresse, Chocolate, Café)", example="Estresse")


class GatilhoOut(BaseModel):
    id: int
    nome: str
    data_criacao: datetime

    class Config:
        from_attributes = True


class GatilhoUpdate(BaseModel):
    nome: constr(strip_whitespace=True,
                 min_length=2, max_length=100) = Field(
                     ..., description="Novo nome para o gatilho")
