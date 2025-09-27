import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# Pega configuração do .env
MYSQL_USER = os.getenv("MYSQL_USER", "diario_user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "senha123")
MYSQL_DB = os.getenv("MYSQL_DB", "diario")
MYSQL_HOST = os.getenv("MYSQL_HOST", "db")
MYSQL_PORT = os.getenv("MYSQL_PORT", 3306)

# Cria URL de conexão
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

# Tenta criar conexão com o DB (até 10 tentativas, esperando 3s cada)
for i in range(10):
    try:
        engine = create_engine(DATABASE_URL, echo=True, future=True)
        with engine.connect() as conn:
            print("Conexão com MySQL bem-sucedida!")
        break
    except OperationalError as e:
        print(f"Tentativa {i+1}/10: Banco de dados ainda não pronto, aguardando 3s...")
        time.sleep(3)
else:
    raise Exception("Não foi possível conectar ao banco de dados.")

# Cria sessão padrão para CRUDs
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
