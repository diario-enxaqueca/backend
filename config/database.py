"""
Configuração do banco de dados usando SQLAlchemy.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import settings

# URL de conexão do banco
DATABASE_URL = (
    f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}"
    f"@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DB}"
)

# Configura parâmetros extras
connect_args = {}

# PRODUCTION: SSL required
if settings.MYSQL_USE_SSL:
    connect_args["ssl"] = {
        "ca": settings.MYSQL_SSL_CA
    }

# Engine do SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verifica conexão antes de usar
    pool_recycle=3600,   # Recicla conexões a cada hora
    echo=settings.DEBUG,  # Log SQL queries em modo debug
    connect_args=connect_args
)

# SessionLocal para criar sessões do banco
# pylint: disable=invalid-name
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os models
Base = declarative_base()


def get_db():
    """
    Dependency para obter sessão do banco de dados.
    Uso: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
