from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Registro(Base):
    __tablename__ = "episodio"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=False)
    data = Column(Date, nullable=False)
    intensidade = Column(Integer, nullable=False)
    descricao = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<Registro(id={self.id}, usuario_id={self.usuario_id}, intensidade={self.intensidade})>"
