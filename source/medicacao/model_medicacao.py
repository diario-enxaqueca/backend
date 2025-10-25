"""
Model para Medicações - Medicamentos utilizados para tratar enxaquecas.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship
from config.database import Base

class Medicacao(Base):
    __tablename__ = "medicacoes"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    nome = Column(String(100), nullable=False)
    dosagem = Column(String(100), nullable=True)  # Ex: "500mg", "1 comprimido"
    data_criacao = Column(DateTime, default=func.now())

    # Relacionamentos
    usuario = relationship("Usuario", backref="medicacoes")

    # Constraint: nome único por usuário
    __table_args__ = (
        UniqueConstraint('usuario_id', 'nome', name='unique_medicacao_por_usuario'),
    )
