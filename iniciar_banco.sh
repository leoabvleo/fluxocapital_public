#!/bin/bash

echo "================================================="
echo "   Configuração do Banco de Dados FluxoCapital   "
echo "================================================="
echo "Este script criará o banco de dados, o usuário padrão"
echo "e importará os dados de teste."
echo ""
echo "Você precisará fornecer a senha do usuário 'root' do MySQL/MariaDB."
echo ""

# Solicitar a senha do root uma vez para não ficar pedindo a cada comando
read -s -p "Digite a senha do root do MySQL/MariaDB: " MYSQL_ROOT_PASSWORD
echo ""

echo "[1/5] Criando o banco de dados 'db_fluxocapital'..."
mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS db_fluxocapital;"

echo "[2/5] Criando o usuário 'user_fluxocapital'..."
# No MariaDB/MySQL mais recente, tentar criar um usuário que já existe pode dar erro. Dropamos se existir e recriamos (ou usamos IF NOT EXISTS dependendo da versao)
mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "CREATE USER IF NOT EXISTS 'user_fluxocapital'@'localhost' IDENTIFIED BY '1qhnTXZDCz8P4cB7n';" 2>/dev/null || mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "ALTER USER 'user_fluxocapital'@'localhost' IDENTIFIED BY '1qhnTXZDCz8P4cB7n';"

echo "[3/5] Concedendo permissões..."
mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "GRANT ALL PRIVILEGES ON db_fluxocapital.* TO 'user_fluxocapital'@'localhost';"

echo "[4/5] Atualizando privilégios..."
mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "FLUSH PRIVILEGES;"

echo "[5/5] Importando dados de teste do arquivo db_fluxocapital_sync.sql..."
if [ -f "db_fluxocapital_sync.sql" ]; then
    mysql -u root -p"$MYSQL_ROOT_PASSWORD" db_fluxocapital < db_fluxocapital_sync.sql
    echo ""
    echo "✅ Banco de dados configurado e populado com sucesso!"
else
    echo "❌ Erro: Arquivo db_fluxocapital_sync.sql não encontrado no diretório atual!"
    exit 1
fi
