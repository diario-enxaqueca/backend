"""
Model para Gatilhos - Fatores que podem desencadear enxaquecas.
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey, text, UniqueConstraint
from sqlalchemy.orm import relationship
from config.database import Base
from source.episodio.model_episodio import episodio_gatilho


# pylint: disable=too-few-public-methods
class Gatilho(Base):
    __tablename__ = "gatilhos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False,
        index=True,
    )
    nome = Column(String(100), nullable=False)
    data_criacao = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    # Relacionamentos
    usuario = relationship("Usuario", backref="gatilhos")

    episodios = relationship("Episodio",
                             secondary=episodio_gatilho,
                             back_populates="gatilhos")

    # Constraint: nome único por usuário
    __table_args__ = (
        UniqueConstraint(
            'usuario_id', 'nome', name='unique_gatilho_por_usuario'
        ),
    )
