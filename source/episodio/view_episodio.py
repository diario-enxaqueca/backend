from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from config.database import get_db
from source.episodio.schemas_episodio import EpisodioCreate, EpisodioOut
from source.usuario.view_usuario import get_current_user  # reusa autenticação

from .controller_episodio import (
    create_episodio, get_episodios_usuario, get_episodio,
    update_episodio, delete_episodio,
)

router = APIRouter()


# --- CRUD endpoints ---


@router.post("/", response_model=EpisodioOut,
             status_code=status.HTTP_201_CREATED, tags=["Episódios"])
def criar_episodio(ep: EpisodioCreate,
                   db: Session = Depends(get_db),
                   user=Depends(get_current_user)):
    episodio = create_episodio(db, usuario_id=user.id, **ep.dict())
    return episodio


@router.get("/", response_model=list[EpisodioOut], tags=["Episódios"])
# pylint: disable=too-many-arguments,too-many-positional-arguments
def listar_episodios(
    skip: int = 0,
    limit: int = Query(100, le=1000),
    data_inicio: date = Query(None, description="Data inicial (YYYY-MM-DD)"),
    data_fim: date = Query(None, description="Data final (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_episodios_usuario(
        db, usuario_id=user.id, skip=skip, limit=limit,
        data_inicio=data_inicio, data_fim=data_fim
    )


@router.get("/{episodio_id}", response_model=EpisodioOut, tags=["Episódios"])
def ver_episodio(episodio_id: int,
                 db: Session = Depends(get_db),
                 user=Depends(get_current_user)):
    episodio = get_episodio(db, episodio_id, usuario_id=user.id)
    if not episodio:
        raise HTTPException(404, detail="Episódio não encontrado")
    return episodio


@router.put("/{episodio_id}", response_model=EpisodioOut, tags=["Episódios"])
def editar_episodio(episodio_id: int,
                    ep: EpisodioCreate,
                    db: Session = Depends(get_db),
                    user=Depends(get_current_user)):
    episodio = get_episodio(db, episodio_id, usuario_id=user.id)
    if not episodio:
        raise HTTPException(404, detail="Episódio não encontrado")
    episodio = update_episodio(db, episodio, **ep.dict())
    return episodio


@router.delete("/{episodio_id}", status_code=204, tags=["Episódios"])
def excluir_episodio(episodio_id: int,
                     db: Session = Depends(get_db),
                     user=Depends(get_current_user)):
    episodio = get_episodio(db, episodio_id, usuario_id=user.id)
    if not episodio:
        raise HTTPException(404, detail="Episódio não encontrado")
    delete_episodio(db, episodio)
