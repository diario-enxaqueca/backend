from sqlalchemy.orm import Session
from config import SessionLocal
from .model_entrada import Entrada

# Criar sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Funções CRUD
def criar_entrada(db: Session, usuario_id: int, data, intensidade: int, descricao: str = None):
    nova = Entrada(usuario_id=usuario_id, data=data, intensidade=intensidade, descricao=descricao)
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

def listar_entradas(db: Session):
    return db.query(Entrada).all()
