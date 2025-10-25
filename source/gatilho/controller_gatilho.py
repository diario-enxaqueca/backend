"""
Controller para Gatilhos - Lógica de negócio para CRUD de gatilhos.
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .model_gatilho import Gatilho

def create_gatilho(db: Session, usuario_id: int, nome: str):
    """Cria um novo gatilho para o usuário."""
    gatilho = Gatilho(usuario_id=usuario_id, nome=nome.strip())
    try:
        db.add(gatilho)
        db.commit()
        db.refresh(gatilho)
        return gatilho
    except IntegrityError:
        db.rollback()
        return None  # Gatilho duplicado para este usuário

def get_gatilhos_usuario(db: Session, usuario_id: int):
    """Lista todos os gatilhos de um usuário, ordenados alfabeticamente."""
    return (
        db.query(Gatilho)
        .filter(Gatilho.usuario_id == usuario_id)
        .order_by(Gatilho.nome)
        .all()
    )

def get_gatilho(db: Session, gatilho_id: int, usuario_id: int):
    """Busca um gatilho específico do usuário."""
    return (
        db.query(Gatilho)
        .filter(Gatilho.id == gatilho_id, Gatilho.usuario_id == usuario_id)
        .first()
    )

def update_gatilho(db: Session, gatilho: Gatilho, nome: str):
    """Atualiza o nome de um gatilho."""
    gatilho.nome = nome.strip()
    try:
        db.commit()
        db.refresh(gatilho)
        return gatilho
    except IntegrityError:
        db.rollback()
        return None  # Nome duplicado

def delete_gatilho(db: Session, gatilho: Gatilho):
    """
    Deleta um gatilho.
    Nota: Associações com episódios são removidas automaticamente (ON DELETE CASCADE).
    """
    db.delete(gatilho)
    db.commit()

def get_gatilho_by_nome(db: Session, usuario_id: int, nome: str):
    """Busca gatilho pelo nome (útil para validação de duplicatas)."""
    return (
        db.query(Gatilho)
        .filter(Gatilho.usuario_id == usuario_id, Gatilho.nome == nome.strip())
        .first()
    )
