#!/bin/sh
set -e

# Recebe host e porta como primeiro argumento
host_port="$1"
shift
cmd="$@"

# Separar host e porta
host=$(echo $host_port | cut -d':' -f1)
port=$(echo $host_port | cut -d':' -f2)

# Se porta não estiver definida, usa 3306
port=${port:-3306}

echo "⏳ Aguardando MySQL ($host:$port)..."

until mysqladmin ping -h"$host" -P"$port" --silent; do
  sleep 2
done

echo "✅ MySQL está pronto, iniciando aplicação..."
exec $cmd

