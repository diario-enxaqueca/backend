from pydantic import BaseModel, Field, conint, constr, validator
from typing import Optional, List
from datetime import date, datetime


class EpisodioCreate(BaseModel):
    data: date = Field(..., description="Data do episódio (YYYY-MM-DD)")
    intensidade: conint(ge=0, le=10) = Field(
        ..., description="Intensidade,0=leve,10=extrema")
    duracao: int = Field(None, description="Duração em minutos")
    observacoes: constr(strip_whitespace=True, max_length=500) = None
    gatilhos: Optional[List[int]] = []           # IDs dos gatilhos
    medicacoes: Optional[List[int]] = []         # IDs das medicações


class EpisodioOut(BaseModel):
    id: int
    data: date
    intensidade: int
    duracao: int = None
    observacoes: str = None
    data_criacao: date
    data_atualizacao: date

    @validator("data_criacao", "data_atualizacao", pre=True)
    def convert_datetime_to_date(cls, value):
        if isinstance(value, datetime):
            return value.date()
        return value

    class Config:
        from_attributes = True
