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
def criar_episodio(db: Session, usuario_id: int, data, intensidade: int, observacoes: str = None):
    novo = Episodio(
        usuario_id=usuario_id,
        data=data,
        intensidade=intensidade,
        observacoes=observacoes
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

def listar_episodios(db: Session):
    return db.query(Episodio).all()

def obter_episodio(db: Session, episodio_id: int):
    return db.query(Episodio).filter(Episodio.id == episodio_id).first()

def atualizar_episodio(db: Session, episodio_id: int, intensidade: int = None, observacoes: str = None):
    episodio = db.query(Episodio).filter(Episodio.id == episodio_id).first()
    if not episodio:
        return None
    if intensidade is not None:
        episodio.intensidade = intensidade
    if observacoes is not None:
        episodio.observacoes = observacoes
    db.commit()
    db.refresh(episodio)
    return episodio

def deletar_episodio(db: Session, episodio_id: int):
    episodio = db.query(Episodio).filter(Episodio.id == episodio_id).first()
    if not episodio:
        return None
    db.delete(episodio)
    db.commit()
    return episodio
