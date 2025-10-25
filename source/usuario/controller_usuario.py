from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .model_usuario import Usuario

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_usuario_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def get_usuario_by_id(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def create_usuario(db: Session, nome: str, email: str, senha: str):
    senha_hash = pwd_context.hash(senha)
    db_usuario = Usuario(nome=nome, email=email, senha_hash=senha_hash)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def authenticate_user(db: Session, email: str, senha: str):
    user = get_usuario_by_email(db, email)
    if user and pwd_context.verify(senha, user.senha_hash):
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
