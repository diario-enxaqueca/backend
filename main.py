from fastapi import FastAPI, APIRouter
from source.entrada.view_entrada import router as entrada_router

# Instância do FastAPI
app = FastAPI(title="Diário de Enxaqueca Backend", version="1.0")

# Router de teste
test_router = APIRouter()

@test_router.get("/")
def teste():
    return {"mensagem": "API funcionando"}

app.include_router(test_router)

# Router de entrada
app.include_router(entrada_router, prefix="/entradas", tags=["Entradas"])
