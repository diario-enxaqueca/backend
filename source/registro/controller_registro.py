from sqlalchemy.orm import Session
from config import SessionLocal
from .model_registro import Registro

# Criar sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Funções CRUD
def criar_registro(db: Session, usuario_id: int, data, intensidade: int, descricao: str = None):
    nova = Registro(usuario_id=usuario_id, data=data, intensidade=intensidade, descricao=descricao)
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

def listar_registros(db: Session):
    return db.query(Registro).all()
