import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# URL do banco de dados (pega do ambiente ou usa padrão)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://usuario:senha123@db:3306/diario"
)

# Tenta criar conexão com o DB (até 10 tentativas, esperando 3s cada)
for i in range(10):
    try:
        engine = create_engine(DATABASE_URL, echo=True, future=True)
        with engine.connect() as conn:
            print("Conexão com MySQL bem-sucedida!")
        break
    except OperationalError:
        print(f"Tentativa {i+1}/10: Banco de dados ainda não pronto, aguardando 3s...")
        time.sleep(3)
else:
    raise Exception("Não foi possível conectar ao banco de dados.")

# Cria sessão padrão para CRUDs
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
