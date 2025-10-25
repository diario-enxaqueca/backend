"""
View (Rotas) para Medicações - Endpoints REST para gerenciar medicações.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, constr, validator
from typing import Optional
from config.database import get_db
from source.usuario.view_usuario import get_current_usuario
from .controller_medicacao import (
    create_medicacao, get_medicacoes_usuario, get_medicacao,
    update_medicacao, delete_medicacao, get_medicacao_by_nome
)
from datetime import datetime

router = APIRouter()

# --- SCHEMAS ---

class MedicacaoCreate(BaseModel):
    nome: constr(strip_whitespace=True, min_length=2, max_length=100) = Field(
        ..., 
        description="Nome da medicação (ex: Paracetamol, Ibuprofeno)",
        example="Paracetamol"
    )
    dosagem: Optional[constr(strip_whitespace=True, max_length=100)] = Field(
        None,
        description="Dosagem opcional (ex: 500mg, 1 comprimido)",
        example="500mg"
    )

class MedicacaoOut(BaseModel):
    id: int
    nome: str
    dosagem: Optional[str] = None
    data_criacao: datetime

    class Config:
        orm_mode = True

class MedicacaoUpdate(BaseModel):
    nome: Optional[constr(strip_whitespace=True, min_length=2, max_length=100)] = Field(
        None, 
        description="Novo nome para a medicação"
    )
    dosagem: Optional[constr(strip_whitespace=True, max_length=100)] = Field(
        None,
        description="Nova dosagem (ou null para remover)"
    )

# --- ROTAS ---

@router.post("/", response_model=MedicacaoOut, status_code=status.HTTP_201_CREATED, tags=["Medicações"])
def criar_medicacao(
    data: MedicacaoCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_usuario)
):
    """
    Cria uma nova medicação para o usuário logado.
    
    **Regras de Negócio:**
    - Nome deve ser único por usuário
    - Dosagem é opcional
    """
    # Verificar se já existe
    if get_medicacao_by_nome(db, user.id, data.nome):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Medicação já cadastrada"
        )
    
    medicacao = create_medicacao(db, usuario_id=user.id, nome=data.nome, dosagem=data.dosagem)
    if not medicacao:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao criar medicação (possível duplicação)"
        )
    return medicacao

@router.get("/", response_model=list[MedicacaoOut], tags=["Medicações"])
def listar_medicacoes(
    db: Session = Depends(get_db),
    user = Depends(get_current_usuario)
):
    """
    Lista todas as medicações do usuário logado, ordenadas alfabeticamente.
    """
    return get_medicacoes_usuario(db, usuario_id=user.id)

@router.get("/{medicacao_id}", response_model=MedicacaoOut, tags=["Medicações"])
def ver_medicacao(
    medicacao_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_usuario)
):
    """
    Visualiza detalhes de uma medicação específica.
    """
    medicacao = get_medicacao(db, medicacao_id, usuario_id=user.id)
    if not medicacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicação não encontrada"
        )
    return medicacao

@router.put("/{medicacao_id}", response_model=MedicacaoOut, tags=["Medicações"])
def editar_medicacao(
    medicacao_id: int,
    data: MedicacaoUpdate,
    db: Session = Depends(get_db),
    user = Depends(get_current_usuario)
):
    """
    Edita uma medicação.
    
    **Regras de Negócio:**
    - Se alterar o nome, deve ser único (não pode duplicar com outra medicação do usuário)
    - Dosagem pode ser atualizada ou removida (enviando null)
    """
    medicacao = get_medicacao(db, medicacao_id, usuario_id=user.id)
    if not medicacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicação não encontrada"
        )
    
    # Se está alterando o nome, verificar duplicatas
    if data.nome:
        existing = get_medicacao_by_nome(db, user.id, data.nome)
        if existing and existing.id != medicacao_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe outra medicação com este nome"
            )
    
    medicacao = update_medicacao(
        db, 
        medicacao, 
        nome=data.nome, 
        dosagem=data.dosagem
    )
    if not medicacao:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao atualizar medicação"
        )
    return medicacao

@router.delete("/{medicacao_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Medicações"])
def excluir_medicacao(
    medicacao_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_usuario)
):
    """
    Exclui uma medicação.
    
    **Nota:** Associações com episódios serão removidas automaticamente.
    """
    medicacao = get_medicacao(db, medicacao_id, usuario_id=user.id)
    if not medicacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicação não encontrada"
        )
    delete_medicacao(db, medicacao)
    return None
