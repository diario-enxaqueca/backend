from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, constr
from config.database import get_db
from .controller_usuario import (
    get_usuario_by_email, create_usuario, authenticate_user,
    update_usuario, delete_usuario, get_usuario_by_id
)
from jose import jwt, JWTError
from config.settings import settings
from datetime import datetime, timedelta

router = APIRouter()

# --- SCHEMAS ---

class UsuarioCreate(BaseModel):
    nome: constr(min_length=3, max_length=100)
    email: EmailStr
    senha: constr(min_length=8, max_length=64)

class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: EmailStr
    data_cadastro: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

# --- JWT ---

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=60))
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

def get_current_usuario(db: Session = Depends(get_db), token: str = Depends(lambda: None)):
    from fastapi.security import OAuth2PasswordBearer
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/usuarios/login")
    try:
        token = token or oauth2_scheme()
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    user = get_usuario_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

# --- ROTAS ---

@router.post("/register", response_model=UsuarioOut, tags=["Usuários"])
def register_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if get_usuario_by_email(db, usuario.email):
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    user = create_usuario(db, usuario.nome, usuario.email, usuario.senha)
    return user

@router.post("/login", response_model=Token, tags=["Usuários"])
def login(form_data: UsuarioCreate, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.email, form_data.senha)
    if not user:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")
    token = create_access_token({"sub": user.email}, expires_delta=timedelta(minutes=60))
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UsuarioOut, tags=["Usuários"])
def read_me(current_user=Depends(get_current_usuario)):
    return current_user

@router.put("/me", response_model=UsuarioOut, tags=["Usuários"])
def update_me(data: UsuarioCreate, db: Session = Depends(get_db), current_user=Depends(get_current_usuario)):
    user = update_usuario(db, current_user, nome=data.nome, email=data.email)
    return user

@router.delete("/me", status_code=204, tags=["Usuários"])
def delete_me(db: Session = Depends(get_db), current_user=Depends(get_current_usuario)):
    delete_usuario(db, current_user)
    return None
