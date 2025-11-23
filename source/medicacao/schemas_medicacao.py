from __future__ import annotations

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, constr

# pylint: disable=too-few-public-methods

# --- SCHEMAS ---


class MedicacaoCreate(BaseModel):
    # pylint: disable=too-few-public-methods
    nome: constr(strip_whitespace=True, min_length=2, max_length=100) = Field(
        ..., description="Nome da medicação (ex: Paracetamol, Ibuprofeno)",
        example="Paracetamol"
    )  # type: ignore
    dosagem: Optional[constr(strip_whitespace=True, max_length=100)] = Field(
        None, description="Dosagem opcional (ex: 500mg, 1 comprimido)",
        example="500mg"
    )  # type: ignore


class MedicacaoOut(BaseModel):
    # pylint: disable=too-few-public-methods
    id: int
    nome: str
    dosagem: Optional[str] = None
    data_criacao: datetime

    class Config:
        from_attributes = True


class MedicacaoUpdate(BaseModel):
    # pylint: disable=too-few-public-methods
    nome: Optional[
        constr(strip_whitespace=True, min_length=2, max_length=100)  # type: ignore
    ] = Field(
        None,
        description="Novo nome para a medicação",
    )
    dosagem: Optional[
        constr(strip_whitespace=True, max_length=100)  # type: ignore
    ] = Field(
        None,
        description="Nova dosagem (ou null para remover)",
    )
