from sqlalchemy import Column, Integer, String, DateTime, text
from config.database import Base


class Usuario(Base):
    # pylint: disable=too-few-public-methods
    __tablename__ = "usuarios"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    data_cadastro = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
