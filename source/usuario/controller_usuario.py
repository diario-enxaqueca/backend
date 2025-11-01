from sqlalchemy.orm import Session
from .model_usuario import Usuario


def get_usuario_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()


def update_usuario(db: Session, usuario: Usuario, nome: str = None, email: str = None):
    if nome:
        usuario.nome = nome
    if email:
        usuario.email = email
    db.commit()
    db.refresh(usuario)
    return usuario


def delete_usuario(db: Session, usuario: Usuario):
    db.delete(usuario)
    db.commit()
