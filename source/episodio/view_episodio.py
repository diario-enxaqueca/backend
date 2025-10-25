from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .controller_episodio import (
    criar_episodio,
    listar_episodios,
    obter_episodio,
    atualizar_episodio,
    deletar_episodio,
    get_db
)

router = APIRouter(prefix="/episodios", tags=["Episodios"])

@router.post("/")
def criar(usuario_id: int, data: str, intensidade: int, observacoes: str = None, db: Session = Depends(get_db)):
    return criar_episodio(db, usuario_id, data, intensidade, observacoes)

@router.get("/")
def listar(db: Session = Depends(get_db)):
    return listar_episodios(db)

@router.get("/{episodio_id}")
def obter(episodio_id: int, db: Session = Depends(get_db)):
    episodio = obter_episodio(db, episodio_id)
    if not episodio:
        raise HTTPException(status_code=404, detail="Episódio não encontrado")
    return episodio

@router.put("/{episodio_id}")
def atualizar(episodio_id: int, intensidade: int = None, observacoes: str = None, db: Session = Depends(get_db)):
    episodio = atualizar_episodio(db, episodio_id, intensidade, observacoes)
    if not episodio:
        raise HTTPException(status_code=404, detail="Episódio não encontrado")
    return episodio

@router.delete("/{episodio_id}")
def deletar(episodio_id: int, db: Session = Depends(get_db)):
    episodio = deletar_episodio(db, episodio_id)
    if not episodio:
        raise HTTPException(status_code=404, detail="Episódio não encontrado")
    return {"detail": "Episódio deletado com sucesso"}
