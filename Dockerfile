FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# ARG MYSQL_ROOT_PASSWORD
# ARG MYSQL_USER
# ARG MYSQL_PASSWORD
# ARG MYSQL_DB
# ARG SECRET_KEY

# ENV MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD
# ENV MYSQL_USER=$MYSQL_USER
# ENV MYSQL_PASSWORD=$MYSQL_PASSWORD
# ENV MYSQL_DB=$MYSQL_DB
# ENV SECRET_KEY=$SECRET_KEY

# # Rodar os testes antes de iniciar a aplicação
# RUN pytest --maxfail=1 --disable-warnings -q

# Expor porta
EXPOSE 8000

# Comando padrão
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
