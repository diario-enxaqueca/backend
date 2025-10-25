from sqlalchemy import Column, Integer, String, Date, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from config.database import Base

class Episodio(Base):
    __tablename__ = "episodios"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    data = Column(Date, nullable=False)
    intensidade = Column(Integer, nullable=False)  # 0 a 10
    duracao = Column(Integer)  # minutos
    observacoes = Column(Text, nullable=True)
    data_criacao = Column(DateTime, default=func.now())
    data_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())

    usuario = relationship("Usuario", backref="episodios")
    # relacionamentos com gatilhos/medicacoes são feitos via tabelas auxiliares
