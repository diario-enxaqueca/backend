from sqlalchemy import Table, Column, Integer, Date, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from config.database import Base


episodio_gatilho = Table(
    "episodio_gatilho",
    Base.metadata,
    Column("episodio_id", Integer, ForeignKey("episodios.id"), primary_key=True),
    Column("gatilho_id", Integer, ForeignKey("gatilhos.id"), primary_key=True),
)

episodio_medicacao = Table(
    "episodio_medicacao",
    Base.metadata,
    Column("episodio_id", Integer, ForeignKey("episodios.id"), primary_key=True),
    Column("medicacao_id", Integer, ForeignKey("medicacoes.id"), primary_key=True),
)


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

    gatilhos = relationship("Gatilho", secondary=episodio_gatilho, back_populates="episodios")
    medicacoes = relationship("Medicacao", secondary=episodio_medicacao, back_populates="episodios")
