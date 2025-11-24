from __future__ import annotations

from typing import Optional, List
from datetime import date, datetime, timedelta

from pydantic import BaseModel, Field, validator

from source.gatilho.schemas_gatilho import GatilhoOut
from source.medicacao.schemas_medicacao import MedicacaoOut

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
    data_inicio: str  # data como string
    data_fim: Optional[str] = None  # calculada se duracao
    intensidade: int
    localizacao: Optional[str] = None  # placeholder, pode ser adicionado ao DB
    sintomas: Optional[str] = None  # placeholder
    observacoes: Optional[str] = None
    usuario_id: int
    gatilhos: List[GatilhoOut] = []
    medicacoes: List[MedicacaoOut] = []

    @validator("data_inicio", pre=True)
    # pylint: disable=no-self-argument
    def convert_data_to_inicio(cls, value):
        if isinstance(value, date):
            return value.isoformat()
        return value

    @validator("data_fim", pre=True)
    # pylint: disable=no-self-argument
    def calculate_data_fim(cls, value, values):
        if 'duracao' in values and values['duracao'] and 'data' in values:
            data = values['data']
            if isinstance(data, date):
                data_fim = (datetime.combine(data, datetime.min.time()) +
                            timedelta(minutes=values['duracao']))
                return data_fim.isoformat()
        return None

    class Config:
        from_attributes = True
    # pylint: disable=too-few-public-methods
