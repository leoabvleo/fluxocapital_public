#!/bin/bash
# Script para rodar o sistema localmente com MySQL (MariaDB)

cd "$(dirname "$0")"

export DB_TYPE=mysql
export DB_USER=user_fluxocapital
export DB_PASS=1qhnTXZDCz8P4cB7n
export DB_HOST=localhost
export DB_NAME=db_fluxocapital

echo "🚀 Iniciando sistema com MySQL local (db_fluxocapital)..."
echo "📡 Acesse: http://127.0.0.1:5001"
echo ""

source venv/bin/activate
python3 app.py
