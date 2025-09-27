# Imagem base
FROM python:3.11-slim

# Cria diretório da aplicação
WORKDIR /app

# Instalar dependências do sistema e cliente MySQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código
COPY . .

# Tornar o script executável
RUN chmod +x /app/wait-for-db.sh

# Expõe porta
EXPOSE 8000

# Comando padrão
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
