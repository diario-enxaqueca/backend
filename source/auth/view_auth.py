from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from config.database import get_db
from config.settings import settings
from source.auth.controller_auth import (
    get_user_by_email, create_user, authenticate_user, create_access_token)
from source.auth.schemas_auth import UserCreate, UserLogin, UserOut, Token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Configuração do FastMail para envio de email
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,  # ex: "seu_email@exemplo.com"
    MAIL_PASSWORD=settings.MAIL_PASSWORD,  # ex: "sua_senha"
    MAIL_FROM=settings.MAIL_FROM,          # ex: "seu_email@exemplo.com"
    MAIL_PORT=settings.MAIL_PORT,          # ex: 587
    MAIL_SERVER=settings.MAIL_SERVER,      # ex: "smtp.exemplo.com"
    MAIL_STARTTLS=settings.MAIL_STARTTLS,            # True/False
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,            # True/False
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


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
def login(form_data: UserLogin, db: Session = Depends(get_db)):
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


# Nova funcionalidade: recuperação de senha


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


RESET_PASSWORD_EXPIRE_MINUTES = 15


def create_reset_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=RESET_PASSWORD_EXPIRE_MINUTES)
    to_encode = {"sub": email, "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def send_reset_email(email_to: EmailStr, token: str):
    reset_url = f"http://localhost:3000/reset-password?token={token}"
    message = MessageSchema(
        subject="Recuperação de senha - Diário de Enxaqueca",
        recipients=[email_to],
        body="Olá,\n\nPara redefinir sua senha, clique no link abaixo:\n"
             + f"{reset_url}\n\n"
             + "Se você não solicitou essa alteração, ignore este email.",
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)


@router.post("/forgot-password", status_code=status.HTTP_200_OK, tags=["auth"])
async def forgot_password(request: ForgotPasswordRequest,
                          background_tasks: BackgroundTasks,
                          db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.email)
    if not user:
        # Responde igual para não revelar se o email está no sistema
        return {"message": "Se o email existir, instruções foram enviadas."}

    token = create_reset_token(user.email)
    background_tasks.add_task(send_reset_email, user.email, token)

    return {"message": "Se o email existir, instruções foram enviadas."}
