from sqlalchemy.orm import Session
from passlib.context import CryptContext
from source.usuario.model_usuario import Usuario
from datetime import datetime, timedelta
from jose import jwt
from config.settings import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
MAX_PASSWORD_LENGTH = 72


def hash_password(senha: str) -> str:
    senha_truncada = senha.encode("utf-8")[:MAX_PASSWORD_LENGTH].decode(
        "utf-8", "ignore")
    return pwd_context.hash(senha_truncada)


def verify_password(senha: str, senha_hash: str) -> bool:
    senha_truncada = senha.encode("utf-8")[:MAX_PASSWORD_LENGTH].decode(
        "utf-8", "ignore")
    return pwd_context.verify(senha_truncada, senha_hash)


def get_user_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()


def create_user(db: Session, nome: str, email: str, senha: str):
    senha_hash = hash_password(senha)
    db_user = Usuario(nome=nome, email=email, senha_hash=senha_hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, senha: str):
    user = get_user_by_email(db, email)
    if user and verify_password(senha, user.senha_hash):
        return user
    return None


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
