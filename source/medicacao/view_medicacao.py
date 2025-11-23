"""
View (Rotas) para Medicações - Endpoints REST para gerenciar medicações.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.database import get_db
from source.usuario.view_usuario import get_current_user
from source.medicacao.schemas_medicacao import (
    MedicacaoCreate, MedicacaoOut, MedicacaoUpdate)
from .controller_medicacao import (
    create_medicacao, get_medicacoes_usuario, get_medicacao,
    delete_medicacao, get_medicacao_by_nome, update_medicacao,
)

router = APIRouter()

# --- ROTAS ---


@router.post("/", response_model=MedicacaoOut,
             status_code=status.HTTP_201_CREATED, tags=["Medicações"])
def criar_medicacao(
    data: MedicacaoCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Cria uma nova medicação para o usuário logado.

    **Regras de Negócio:**
    - Nome deve ser único por usuário
    - Dosagem é opcional
    """
    if get_medicacao_by_nome(db, user.id, data.nome):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Medicação já cadastrada"
        )

    medicacao = create_medicacao(
        db, usuario_id=user.id,
        nome=data.nome, dosagem=data.dosagem)
    if not medicacao:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao criar medicação (possível duplicação)"
        )
    return medicacao


@router.get("/", response_model=list[MedicacaoOut], tags=["Medicações"])
def listar_medicacoes(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Lista todas as medicações do usuário logado, ordenadas alfabeticamente.
    """
    return get_medicacoes_usuario(db, usuario_id=user.id)


@router.get(
    "/{medicacao_id}", response_model=MedicacaoOut, tags=["Medicações"]
)
def ver_medicacao(
    medicacao_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
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


@router.put(
    "/{medicacao_id}", response_model=MedicacaoOut, tags=["Medicações"]
)
def editar_medicacao(
    medicacao_id: int,
    data: MedicacaoUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    medicacao = get_medicacao(db, medicacao_id, usuario_id=user.id)
    if not medicacao:
        raise HTTPException(status_code=404, detail="Medicação não encontrada")

    if data.nome is not None:
        existing = get_medicacao_by_nome(db, user.id, data.nome)
        if existing and existing.id != medicacao_id:
            raise HTTPException(
                status_code=400,
                detail="Já existe outra medicação com este nome")

    updated_medicacao = update_medicacao(
        db,
        medicacao,
        nome=data.nome,
        dosagem=data.dosagem
    )

    if updated_medicacao is None:
        raise HTTPException(
            status_code=400,
            detail="Erro ao atualizar medicação"
        )

    return updated_medicacao


@router.delete("/{medicacao_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               tags=["Medicações"])
def excluir_medicacao(
    medicacao_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
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
    # Retorna 204 No Content quando excluído com sucesso
