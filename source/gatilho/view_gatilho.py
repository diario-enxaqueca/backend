"""
View (Rotas) para Gatilhos - Endpoints REST para gerenciar gatilhos.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.database import get_db
from source.usuario.view_usuario import get_current_user
from .controller_gatilho import (
    create_gatilho, get_gatilhos_usuario, get_gatilho,
    update_gatilho, delete_gatilho, get_gatilho_by_nome
)
from .schemas_gatilho import GatilhoCreate, GatilhoOut, GatilhoUpdate

router = APIRouter()


# --- ROTAS ---


@router.post("/", response_model=GatilhoOut,
             status_code=status.HTTP_201_CREATED,
             tags=["Gatilhos"])
def criar_gatilho(
    data: GatilhoCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Cria um novo gatilho para o usuário logado.

    **Regras de Negócio:**
    - Nome deve ser único por usuário
    - Nome é case-sensitive e será salvo com espaços removidos
    """
    if get_gatilho_by_nome(db, user.id, data.nome):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Gatilho já cadastrado"
        )

    gatilho = create_gatilho(db, usuario_id=user.id, nome=data.nome)
    if not gatilho:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao criar gatilho (possível duplicação)"
        )
    return gatilho


@router.get("/", response_model=list[GatilhoOut], tags=["Gatilhos"])
def listar_gatilhos(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Lista todos os gatilhos do usuário logado, ordenados alfabeticamente.
    """
    return get_gatilhos_usuario(db, usuario_id=user.id)


@router.get("/{gatilho_id}", response_model=GatilhoOut, tags=["Gatilhos"])
def ver_gatilho(
    gatilho_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Visualiza detalhes de um gatilho específico.
    """
    gatilho = get_gatilho(db, gatilho_id, usuario_id=user.id)
    if not gatilho:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gatilho não encontrado"
        )
    return gatilho


@router.put("/{gatilho_id}", response_model=GatilhoOut, tags=["Gatilhos"])
def editar_gatilho(
    gatilho_id: int,
    data: GatilhoUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Edita o nome de um gatilho.

    **Regras de Negócio:**
    - Novo nome deve ser único (não pode duplicar com outro gatilho do usuário)
    """
    gatilho = get_gatilho(db, gatilho_id, usuario_id=user.id)
    if not gatilho:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gatilho não encontrado"
        )

    existing = get_gatilho_by_nome(db, user.id, data.nome)
    if existing and existing.id != gatilho_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe outro gatilho com este nome"
        )

    gatilho = update_gatilho(db, gatilho, nome=data.nome)
    if not gatilho:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao atualizar gatilho"
        )
    return gatilho


@router.delete("/{gatilho_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               tags=["Gatilhos"])
def excluir_gatilho(
    gatilho_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Exclui um gatilho.

    **Nota:** Associações com episódios serão removidas automaticamente.
    """
    gatilho = get_gatilho(db, gatilho_id, usuario_id=user.id)
    if not gatilho:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gatilho não encontrado"
        )
    delete_gatilho(db, gatilho)
    # endpoint retorna 204 No Content quando excluído com sucesso
