from __future__ import annotations

from typing import Optional, List
from datetime import date, datetime

from pydantic import BaseModel, Field, validator

# pylint: disable=too-few-public-methods


class EpisodioCreate(BaseModel):
    data: date = Field(..., description="Data do episódio (YYYY-MM-DD)")
    intensidade: int = Field(
        ..., ge=0, le=10, description="Intensidade,0=leve,10=extrema"
    )
    duracao: int = Field(None, description="Duração em minutos")
    observacoes: Optional[str] = Field(
        None,
        max_length=500,
        description="Observações do episódio",
    )
    gatilhos: Optional[List[int]] = []  # IDs dos gatilhos
    medicacoes: Optional[List[int]] = []  # IDs das medicações


class EpisodioOut(BaseModel):
    id: int
    data: date
    intensidade: int
    duracao: int = None
    observacoes: str = None
    data_criacao: date
    data_atualizacao: date

    @validator("data_criacao", "data_atualizacao", pre=True)
    # pylint: disable=no-self-argument
    def convert_datetime_to_date(cls, value):
        if isinstance(value, datetime):
            return value.date()
        return value

    class Config:
        from_attributes = True
    # pylint: disable=too-few-public-methods
