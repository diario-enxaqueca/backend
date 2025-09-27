from config import engine

try:
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        print("Conexão com MySQL bem-sucedida:", result.scalar())
except Exception as e:
    print("Erro ao conectar no banco:", e)
