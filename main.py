from fastapi import FastAPI, APIRouter
from source.registro.view_registro import router as registro_router

# Instância do FastAPI
app = FastAPI(title="Diário de Enxaqueca Backend", version="1.0")

# Router de teste
test_router = APIRouter()

@test_router.get("/")
def teste():
    return {"mensagem": "API funcionando"}

app.include_router(test_router)

# Router de registro
app.include_router(registro_router, prefix="/registros", tags=["registros"])
