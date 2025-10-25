from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Episodio(Base):
    __tablename__ = "episodio"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    data = Column(Date, nullable=False)
    intensidade = Column(Integer, nullable=False)  # 0–10
    observacoes = Column(String(500), nullable=True)
    criado_em = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return (
            f"<Episodio(id={self.id}, usuario_id={self.usuario_id}, "
            f"data={self.data}, intensidade={self.intensidade})>"
        )
