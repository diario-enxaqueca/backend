from sqlalchemy.orm import Session
from config import SessionLocal
from .model_episodio import Episodio

# Criar sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Funções CRUD
def criar_episodio(db: Session, usuario_id: int, data, intensidade: int, descricao: str = None):
    nova = Episodio(usuario_id=usuario_id, data=data, intensidade=intensidade, descricao=descricao)
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

def listar_episodio(db: Session):
    return db.query(Episodio).all()
