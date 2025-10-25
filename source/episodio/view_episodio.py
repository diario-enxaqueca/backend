from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, conint, constr, validator
from config.database import get_db
from source.usuario.view_usuario import get_current_usuario  # reusa autenticação
from .controller_episodio import (
    create_episodio, get_episodios_usuario, get_episodio,
    update_episodio, delete_episodio
)
from datetime import date

router = APIRouter()

class EpisodioCreate(BaseModel):
    data: date = Field(..., description="Data do episódio (YYYY-MM-DD)")
    intensidade: conint(ge=0, le=10) = Field(..., description="Intensidade, 0=leve, 10=extrema")
    duracao: int = Field(None, description="Duração em minutos")
    observacoes: constr(strip_whitespace=True, max_length=500) = None

class EpisodioOut(BaseModel):
    id: int
    data: date
    intensidade: int
    duracao: int = None
    observacoes: str = None
    data_criacao: date
    data_atualizacao: date

    class Config:
        orm_mode = True

# --- CRUD endpoints ---

@router.post("/", response_model=EpisodioOut, status_code=status.HTTP_201_CREATED, tags=["Episódios"])
def criar_episodio(ep: EpisodioCreate, db: Session = Depends(get_db), user = Depends(get_current_usuario)):
    episodio = create_episodio(db, usuario_id=user.id, **ep.dict())
    return episodio

@router.get("/", response_model=list[EpisodioOut], tags=["Episódios"])
def listar_episodios(
    skip: int = 0,
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db),
    user = Depends(get_current_usuario)
):
    return get_episodios_usuario(db, usuario_id=user.id, skip=skip, limit=limit)

@router.get("/{episodio_id}", response_model=EpisodioOut, tags=["Episódios"])
def ver_episodio(episodio_id: int, db: Session = Depends(get_db), user = Depends(get_current_usuario)):
    episodio = get_episodio(db, episodio_id, usuario_id=user.id)
    if not episodio:
        raise HTTPException(404, detail="Episódio não encontrado")
    return episodio

@router.put("/{episodio_id}", response_model=EpisodioOut, tags=["Episódios"])
def editar_episodio(episodio_id: int, ep: EpisodioCreate, db: Session = Depends(get_db), user = Depends(get_current_usuario)):
    episodio = get_episodio(db, episodio_id, usuario_id=user.id)
    if not episodio:
        raise HTTPException(404, detail="Episódio não encontrado")
    episodio = update_episodio(db, episodio, **ep.dict())
    return episodio

@router.delete("/{episodio_id}", status_code=204, tags=["Episódios"])
def excluir_episodio(episodio_id: int, db: Session = Depends(get_db), user = Depends(get_current_usuario)):
    episodio = get_episodio(db, episodio_id, usuario_id=user.id)
    if not episodio:
        raise HTTPException(404, detail="Episódio não encontrado")
    delete_episodio(db, episodio)
