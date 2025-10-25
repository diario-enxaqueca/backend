from sqlalchemy.orm import Session
from .model_episodio import Episodio

def create_episodio(db: Session, usuario_id: int, data: str, intensidade: int, duracao: int = None, observacoes: str = None):
    episodio = Episodio(
        usuario_id=usuario_id,
        data=data,
        intensidade=intensidade,
        duracao=duracao,
        observacoes=observacoes
    )
    db.add(episodio)
    db.commit()
    db.refresh(episodio)
    return episodio

def get_episodios_usuario(db: Session, usuario_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(Episodio)
        .filter(Episodio.usuario_id == usuario_id)
        .order_by(Episodio.data.desc())
        .offset(skip).limit(limit)
        .all()
    )

def get_episodio(db: Session, episodio_id: int, usuario_id: int):
    return (
        db.query(Episodio)
        .filter(Episodio.id == episodio_id, Episodio.usuario_id == usuario_id)
        .first()
    )

def update_episodio(db: Session, episodio: Episodio, **kwargs):
    for field, value in kwargs.items():
        if hasattr(episodio, field) and value is not None:
            setattr(episodio, field, value)
    db.commit()
    db.refresh(episodio)
    return episodio

def delete_episodio(db: Session, episodio: Episodio):
    db.delete(episodio)
    db.commit()
