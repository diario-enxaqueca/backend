#!/bin/bash
# Script para aguardar MySQL estar pronto

set -e

echo "==================================="
echo "Aguardando MySQL ficar disponível..."
echo "Host: ${MYSQL_HOST}"
echo "Port: ${MYSQL_PORT}"
echo "User: ${MYSQL_USER}"
echo "Database: ${MYSQL_DB}"
echo "==================================="

# Aguarda até 60 segundos
TIMEOUT=60
COUNTER=0

until mysql -h"${MYSQL_HOST}" -P"${MYSQL_PORT}" -u"${MYSQL_USER}" -p"${MYSQL_PASSWORD}" -e "SELECT 1" > /dev/null 2>&1; do
  echo "MySQL ainda não está pronto - aguardando... (${COUNTER}s)"
  sleep 2
  COUNTER=$((COUNTER + 2))
  
  if [ $COUNTER -ge $TIMEOUT ]; then
    echo "ERRO: Timeout ao aguardar MySQL após ${TIMEOUT} segundos"
    echo "Verifique se o container MySQL está rodando e as credenciais estão corretas"
    exit 1
  fi
done

echo "==================================="
echo "✅ MySQL está pronto!"
echo "==================================="

# Executar comando passado como argumento
exec "$@"
