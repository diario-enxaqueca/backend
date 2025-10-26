"""
View (Rotas) para Usuários - Endpoints REST.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, constr
from config.database import get_db
from .controller_usuario import (
    get_usuario_by_email, create_usuario, authenticate_user,
    update_usuario, delete_usuario)
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from config.settings import settings
from datetime import datetime, timedelta

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/usuarios/login")

# --- SCHEMAS ---


class UsuarioCreate(BaseModel):
    nome: constr(min_length=3, max_length=100)
    email: EmailStr
    senha: constr(min_length=8, max_length=72)  # Limite fixado

    class Config:
        from_attributes = True


class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: EmailStr
    data_cadastro: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

# --- JWT ---


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def get_current_usuario(db: Session = Depends(get_db),
                        token: str = Depends(oauth2_scheme)):
    """
    Dependency para obter usuário autenticado a partir do token JWT.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_usuario_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user

# --- ROTAS ---


@router.post("/register", response_model=UsuarioOut,
             status_code=status.HTTP_201_CREATED, tags=["Usuários"])
def register_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Registra novo usuário.

    **Regras:**
    - Email deve ser único
    - Senha: 8-72 caracteres (limite do bcrypt)
    """
    if get_usuario_by_email(db, usuario.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado"
        )
    user = create_usuario(db, usuario.nome, usuario.email, usuario.senha)
    return user


@router.post("/login", response_model=Token, tags=["Usuários"])
def login(form_data: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Autentica usuário e retorna token JWT.
    """
    user = authenticate_user(db, form_data.email, form_data.senha)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UsuarioOut, tags=["Usuários"])
def read_me(current_user=Depends(get_current_usuario)):
    return current_user


@router.put("/me", response_model=UsuarioOut, tags=["Usuários"])
def update_me(data: UsuarioCreate, db: Session = Depends(get_db),
              current_user=Depends(get_current_usuario)):
    user = update_usuario(db, current_user, nome=data.nome, email=data.email)
    return user


@router.delete("/me", status_code=204, tags=["Usuários"])
def delete_me(db: Session = Depends(get_db),
              current_user=Depends(get_current_usuario)):
    delete_usuario(db, current_user)
    return None
