from sqlalchemy.orm import Session
from passlib.context import CryptContext

from .model_usuario import Usuario

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
MAX_PASSWORD_LENGTH = 72


def hash_password(senha: str) -> str:
    senha_truncada = senha.encode("utf-8")[:MAX_PASSWORD_LENGTH].decode(
        "utf-8", "ignore")
    return pwd_context.hash(senha_truncada)


def create_usuario(db: Session, nome: str, email: str, senha: str):
    senha_hash = hash_password(senha)
    db_user = Usuario(nome=nome, email=email, senha_hash=senha_hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_usuario_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()


def update_usuario(
    db: Session,
    usuario: Usuario,
    nome: str = None,
    email: str = None,
):
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
