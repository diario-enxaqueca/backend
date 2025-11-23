"""
View (Rotas) para Usuários - Endpoints REST.
Agora integrado com serviço externo de autenticação.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from config.database import get_db
from config.settings import settings

from source.usuario.schemas_usuario import UserUpdate, UserCreate, UserOut
from .controller_usuario import (
    update_usuario,
    delete_usuario,
    get_usuario_by_email,
    create_usuario,
)


router = APIRouter()
# O token será recebido no cabeçalho Authorization e validado localmente
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# --- AUTENTICAÇÃO E AUTORIZAÇÃO ---


def get_current_user(db: Session = Depends(get_db),
                     token: str = Depends(oauth2_scheme)):
    """
    Dependency para obter usuário autenticado a partir do token JWT.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc

    user = get_usuario_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user

# --- ROTAS ---


@router.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Usuários"],
)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if get_usuario_by_email(db, user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="E-mail já cadastrado")
    return create_usuario(db, user.nome, user.email, user.senha)

# --- ROTAS ---


@router.get("/me", response_model=UserOut, tags=["Usuários"])
def read_me(current_user=Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserOut, tags=["Usuários"])
def update_me(data: UserUpdate,
              db: Session = Depends(get_db),
              current_user=Depends(get_current_user)):
    user = update_usuario(db, current_user, nome=data.nome, email=data.email)
    return user


@router.delete("/me", status_code=204, tags=["Usuários"])
def delete_me(db: Session = Depends(get_db),
              current_user=Depends(get_current_user)):
    delete_usuario(db, current_user)
    # Retorna 204 No Content quando a exclusão ocorre com sucesso
