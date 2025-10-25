"""
Controller para Medicações - Lógica de negócio para CRUD de medicações.
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .model_medicacao import Medicacao

def create_medicacao(db: Session, usuario_id: int, nome: str, dosagem: str = None):
    """Cria uma nova medicação para o usuário."""
    medicacao = Medicacao(
        usuario_id=usuario_id,
        nome=nome.strip(),
        dosagem=dosagem.strip() if dosagem else None
    )
    try:
        db.add(medicacao)
        db.commit()
        db.refresh(medicacao)
        return medicacao
    except IntegrityError:
        db.rollback()
        return None  # Medicação duplicada para este usuário

def get_medicacoes_usuario(db: Session, usuario_id: int):
    """Lista todas as medicações de um usuário, ordenadas alfabeticamente."""
    return (
        db.query(Medicacao)
        .filter(Medicacao.usuario_id == usuario_id)
        .order_by(Medicacao.nome)
        .all()
    )

def get_medicacao(db: Session, medicacao_id: int, usuario_id: int):
    """Busca uma medicação específica do usuário."""
    return (
        db.query(Medicacao)
        .filter(Medicacao.id == medicacao_id, Medicacao.usuario_id == usuario_id)
        .first()
    )

def update_medicacao(db: Session, medicacao: Medicacao, nome: str = None, dosagem: str = None):
    """Atualiza uma medicação."""
    if nome:
        medicacao.nome = nome.strip()
    if dosagem is not None:  # Permite definir como None
        medicacao.dosagem = dosagem.strip() if dosagem else None
    
    try:
        db.commit()
        db.refresh(medicacao)
        return medicacao
    except IntegrityError:
        db.rollback()
        return None  # Nome duplicado

def delete_medicacao(db: Session, medicacao: Medicacao):
    """
    Deleta uma medicação.
    Nota: Associações com episódios são removidas automaticamente (ON DELETE CASCADE).
    """
    db.delete(medicacao)
    db.commit()

def get_medicacao_by_nome(db: Session, usuario_id: int, nome: str):
    """Busca medicação pelo nome (útil para validação de duplicatas)."""
    return (
        db.query(Medicacao)
        .filter(Medicacao.usuario_id == usuario_id, Medicacao.nome == nome.strip())
        .first()
    )
