from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .controller_registro import criar_registro, listar_registros, get_db

router = APIRouter()

@router.post("/")
def criar(usuario_id: int, data: str, intensidade: int, descricao: str = None, db: Session = Depends(get_db)):
    return criar_registro(db, usuario_id, data, intensidade, descricao)

@router.get("/")
def listar(db: Session = Depends(get_db)):
    return listar_registros(db)
