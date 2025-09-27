from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .controller_entrada import criar_entrada, listar_entradas, get_db

router = APIRouter()

@router.post("/")
def criar(usuario_id: int, data: str, intensidade: int, descricao: str = None, db: Session = Depends(get_db)):
    return criar_entrada(db, usuario_id, data, intensidade, descricao)

@router.get("/")
def listar(db: Session = Depends(get_db)):
    return listar_entradas(db)
