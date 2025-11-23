"""
Ponto de entrada da aplicação FastAPI - Diário de Enxaqueca.
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError
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
    """Cria tabelas ao iniciar (se não existirem).
    
    create_all() usa CREATE TABLE IF NOT EXISTS, então:
    - Não apaga dados existentes
    - Garante que tabelas existam em qualquer restart
    - init.sql ainda é responsável pelos INSERTs iniciais
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tabelas backend verificadas/criadas")
    except OperationalError as exc:
        logger.error("Erro ao criar tabelas: %s", exc)


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
