from typing import Optional, List, Union
from datetime import date

from sqlalchemy.orm import Session, joinedload

from source.gatilho.model_gatilho import Gatilho
from source.medicacao.model_medicacao import Medicacao

from .model_episodio import Episodio


# pylint: disable=too-many-arguments, too-many-positional-arguments
def create_episodio(
    db: Session,
    usuario_id: int,
    data: Union[str, date],
    intensidade: int,
    duracao: int = None,
    observacoes: str = None,
    gatilhos: Optional[List[int]] = None,
    medicacoes: Optional[List[int]] = None,
):
    # Converter string para date se necessário
    if isinstance(data, str):
        data = date.fromisoformat(data)

    episodio = Episodio(
        usuario_id=usuario_id,
        data=data,
        intensidade=intensidade,
        duracao=duracao,
        observacoes=observacoes
    )
    db.add(episodio)
    db.commit()
    db.refresh(episodio)

    if gatilhos:
        gatilhos_objs = (
            db.query(Gatilho)
            .filter(Gatilho.id.in_(gatilhos))
            .all()
        )
        episodio.gatilhos.extend(gatilhos_objs)
    if medicacoes:
        medicacoes_objs = (
            db.query(Medicacao)
            .filter(Medicacao.id.in_(medicacoes))
            .all()
        )
        episodio.medicacoes.extend(medicacoes_objs)

    db.commit()
    return episodio


def get_episodios_usuario(
    db: Session,
    usuario_id: int,
    skip: int = 0,
    limit: int = 10,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
):
    query = (
        db.query(Episodio)
        .options(joinedload(Episodio.gatilhos),
                 joinedload(Episodio.medicacoes))
        .filter(Episodio.usuario_id == usuario_id)
    )
    if data_inicio:
        query = query.filter(Episodio.data >= data_inicio)
    if data_fim:
        query = query.filter(Episodio.data <= data_fim)
    return (
        query
        .order_by(Episodio.data.desc())
        .offset(skip).limit(limit)
        .all()
    )


def get_episodio(db: Session, episodio_id: int, usuario_id: int):
    return (
        db.query(Episodio)
        .options(joinedload(Episodio.gatilhos),
                 joinedload(Episodio.medicacoes))
        .filter(Episodio.id == episodio_id, Episodio.usuario_id == usuario_id)
        .first()
    )


def update_episodio(db: Session, episodio: Episodio, **kwargs):
    for field, value in kwargs.items():
        if hasattr(episodio, field) and value is not None:
            setattr(episodio, field, value)
    db.commit()
    db.refresh(episodio)
    return episodio


def delete_episodio(db: Session, episodio: Episodio):
    db.delete(episodio)
    db.commit()
