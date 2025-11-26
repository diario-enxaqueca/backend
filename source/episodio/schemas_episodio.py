from __future__ import annotations

from typing import Optional, List
from datetime import date

from pydantic import BaseModel, Field, field_validator, ConfigDict

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
    data_inicio: str = Field(alias="data")  # alias to map from model.data
    data_fim: Optional[str] = None  # calculada se duracao
    intensidade: int
    localizacao: Optional[str] = None  # placeholder, pode ser adicionado ao DB
    sintomas: Optional[str] = None  # placeholder
    observacoes: Optional[str] = None
    usuario_id: int
    gatilhos: List[GatilhoOut] = []
    medicacoes: List[MedicacaoOut] = []

    @field_validator("data_inicio", mode='before')
    # pylint: disable=no-self-argument
    def convert_data_to_inicio(cls, value):
        if isinstance(value, date):
            return value.isoformat()
        return value

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

# pylint: disable=too-few-public-methods
