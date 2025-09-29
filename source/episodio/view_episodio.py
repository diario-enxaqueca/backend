from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .controller_episodio import criar_episodio, listar_episodio, get_db

router = APIRouter()

@router.post("/")
def criar(usuario_id: int, data: str, intensidade: int, descricao: str = None, db: Session = Depends(get_db)):
    return criar_episodio(db, usuario_id, data, intensidade, descricao)

@router.get("/")
def listar(db: Session = Depends(get_db)):
    return listar_episodio(db)
