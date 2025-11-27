"""
Configurações centralizadas da aplicação usando Pydantic Settings.
"""
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação carregadas do .env"""

    # Banco de Dados
    MYSQL_ROOT_PASSWORD: str | None = None
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str
    MYSQL_HOST: str = "db"
    MYSQL_PORT: int = 3306
    MYSQL_USE_SSL: bool = False
    MYSQL_SSL_CA: str | None = None

    # Aplicação
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 horas

    # Ambiente
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    FRONTEND_URL: str = "http://localhost:3000"

    # Configurações de email SMTP para FastMail
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int = 587
    MAIL_SERVER: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False

    # Configuração do Pydantic V2
    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", ".env"),
        case_sensitive=True,
        extra="ignore"  # ✅ Ignora campos extras do .env
    )


# Instância global de configurações
settings = Settings()
