"""Utilitários compartilhados da aplicação."""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
MAX_PASSWORD_LENGTH = 72


def hash_password(senha: str) -> str:
    """Hash uma senha usando Argon2."""
    senha_truncada = senha.encode("utf-8")[:MAX_PASSWORD_LENGTH].decode(
        "utf-8", "ignore")
    return pwd_context.hash(senha_truncada)


def verify_password(senha: str, senha_hash: str) -> bool:
    """Verifica se uma senha corresponde ao hash."""
    return pwd_context.verify(senha, senha_hash)
