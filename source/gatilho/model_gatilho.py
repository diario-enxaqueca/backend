"""
Model para Gatilhos - Fatores que podem desencadear enxaquecas.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship
from config.database import Base

class Gatilho(Base):
    __tablename__ = "gatilhos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    nome = Column(String(100), nullable=False)
    data_criacao = Column(DateTime, default=func.now())

    # Relacionamentos
    usuario = relationship("Usuario", backref="gatilhos")

    # Constraint: nome único por usuário
    __table_args__ = (
        UniqueConstraint('usuario_id', 'nome', name='unique_gatilho_por_usuario'),
    )
