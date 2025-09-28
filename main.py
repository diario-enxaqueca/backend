from fastapi import FastAPI, APIRouter
from source.episodio.view_episodio import router as episodio_router

# Instância do FastAPI
app = FastAPI(title="Diário de Enxaqueca Backend", version="1.0")

# Router de teste
test_router = APIRouter()

@test_router.get("/")
def teste():
    return {"mensagem": "API funcionando"}

app.include_router(test_router)

# Router de episodio
app.include_router(episodio_router, prefix="/episodio", tags=["episodio"])
