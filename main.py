"""
Ponto de entrada da aplicação FastAPI - Diário de Enxaqueca.
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy import text
from config.settings import settings
from config.database import Base, engine

# Importar rotas (views)
from source.usuario.view_usuario import router as usuario_router
from source.episodio.view_episodio import router as episodio_router
from source.gatilho.view_gatilho import router as gatilho_router
from source.medicacao.view_medicacao import router as medicacao_router

# Importar todos os modelos para registrar no metadata
# pylint: disable=W0611
from source.usuario.model_usuario import Usuario  # noqa: F401
from source.episodio.model_episodio import Episodio  # noqa: F401
from source.gatilho.model_gatilho import Gatilho  # noqa: F401
from source.medicacao.model_medicacao import Medicacao  # noqa: F401

# Autenticação movida para repositório separado `autenticacao`

logger = logging.getLogger("uvicorn")

# Criar instância do FastAPI
app = FastAPI(
    title="Diário de Enxaqueca API",
    description="API REST para gerenciamento de episódios de enxaqueca",
    version="1.0.0",
    debug=settings.DEBUG
)

origins = [
    "http://localhost:3000",     # URL do frontend local dev
    "http://frontend",           # Nome do serviço frontend no Docker
    # Você pode adicionar outras origens permitidas aqui
]

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Em produção, especificar domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(usuario_router, prefix="/api/usuarios",
                   tags=["Usuários"])
app.include_router(episodio_router, prefix="/api/episodios",
                   tags=["Episódios"])
app.include_router(gatilho_router, prefix="/api/gatilhos",
                   tags=["Gatilhos"])
app.include_router(medicacao_router, prefix="/api/medicacoes",
                   tags=["Medicações"])
# rotas de autenticação ficam em serviço separado


@app.on_event("startup")
def startup_event():
    """Verifica existência das tabelas e cria somente as ausentes.

    Também loga contagem de registros para diagnosticar perda de dados.
    """
    try:
        with engine.connect() as conn:
            # Verificar se tabela principal já existe
            result = conn.execute(
                text(
                    "SELECT COUNT(*) FROM information_schema.tables "
                    "WHERE table_schema = :db AND table_name = 'usuarios'"
                ),
                {"db": settings.MYSQL_DB},
            ).scalar()
            if result == 0:
                # Nenhuma tabela 'usuarios' -> cria todas as definidas
                Base.metadata.create_all(bind=conn)
                logger.info(
                    "Tabelas backend criadas (usuarios ausente)"
                )
            else:
                logger.info("Tabela usuarios já existe; pulando create_all")

            # Logar contagem de linhas para diagnóstico
            for tbl in ["usuarios", "episodios", "gatilhos", "medicacoes"]:
                try:
                    count = conn.execute(
                        text(f"SELECT COUNT(*) FROM {tbl}")
                    ).scalar()
                    logger.info("Tabela %s possui %d registros", tbl, count)
                except SQLAlchemyError as inner_exc:
                    logger.warning(
                        "Falha ao contar registros em %s: %s",
                        tbl,
                        inner_exc,
                    )
    except OperationalError as exc:
        logger.error("Erro ao verificar/criar tabelas: %s", exc)


@app.get("/")
async def root():
    """Endpoint raiz para verificar se a API está funcionando."""
    return {
        "message": "Diário de Enxaqueca API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
