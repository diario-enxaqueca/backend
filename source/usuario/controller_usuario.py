"""
Controller para Usuários - Lógica de negócio e segurança de senhas.
"""
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .model_usuario import Usuario

# Configuração do bcrypt
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Limite de senha do bcrypt
MAX_PASSWORD_LENGTH = 72


def hash_password(senha: str) -> str:
    """Gera hash truncando a senha se for exceder o limite de 72 bytes."""
    senha_truncada = senha.encode("utf-8")[:MAX_PASSWORD_LENGTH].decode("utf-8",
                                                                        "ignore")
    return pwd_context.hash(senha_truncada)


def verify_password(senha: str, senha_hash: str) -> bool:
    """Verifica a senha truncando antes de comparar."""
    senha_truncada = senha.encode("utf-8")[:MAX_PASSWORD_LENGTH].decode("utf-8",
                                                                        "ignore")
    return pwd_context.verify(senha_truncada, senha_hash)


def get_usuario_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()


def get_usuario_by_id(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()


def create_usuario(db: Session, nome: str, email: str, senha: str):
    senha_hash = hash_password(senha)
    db_usuario = Usuario(nome=nome, email=email, senha_hash=senha_hash)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def authenticate_user(db: Session, email: str, senha: str):
    user = get_usuario_by_email(db, email)
    if user and verify_password(senha, user.senha_hash):
        return user
    return None


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
