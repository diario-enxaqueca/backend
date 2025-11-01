from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from source.auth.schemas_auth import UserCreate, UserOut, Token
from source.auth.controller_auth import (
    get_user_by_email, create_user, authenticate_user, create_access_token
)
from config.database import get_db
from config.settings import settings
from jose import JWTError, jwt
from datetime import timedelta

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


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
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user


@router.post("/register", response_model=UserOut,
             status_code=status.HTTP_201_CREATED, tags=["auth"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="E-mail já cadastrado")
    return create_user(db, user.nome, user.email, user.senha)


@router.post("/login", response_model=Token, tags=["auth"])
def login(form_data: UserCreate, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.email, form_data.senha)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="E-mail ou senha incorretos")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": user.email},
                                expires_delta=access_token_expires)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut, tags=["auth"])
def read_me(current_user=Depends(get_current_user)):
    return current_user
