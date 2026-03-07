#!/bin/bash

echo "================================================="
echo "   Configuração do Banco de Dados FluxoCapital   "
echo "================================================="
echo "Este script criará o banco de dados, o usuário padrão"
echo "e importará os dados de teste."
echo ""

# Tenta conectar como root sem senha primeiro
if mysql -u root -e "exit" 2>/dev/null; then
    echo "Identificado: MySQL root sem senha."
    MYSQL_CMD="mysql -u root"
else
    echo "MySQL root exige senha ou acesso negado."
    read -s -p "Digite a senha do root do MySQL/MariaDB: " MYSQL_ROOT_PASSWORD
    echo ""
    MYSQL_CMD="mysql -u root -p$MYSQL_ROOT_PASSWORD"
fi

echo "[1/5] Criando o banco de dados 'db_fluxocapital'..."
$MYSQL_CMD -e "CREATE DATABASE IF NOT EXISTS db_fluxocapital;"

echo "[2/5] Criando o usuário 'user_fluxocapital'..."
$MYSQL_CMD -e "CREATE USER IF NOT EXISTS 'user_fluxocapital'@'localhost' IDENTIFIED BY '1qhnTXZDCz8P4cB7n';" 2>/dev/null || $MYSQL_CMD -e "ALTER USER 'user_fluxocapital'@'localhost' IDENTIFIED BY '1qhnTXZDCz8P4cB7n';"

echo "[3/5] Concedendo permissões..."
$MYSQL_CMD -e "GRANT ALL PRIVILEGES ON db_fluxocapital.* TO 'user_fluxocapital'@'localhost';"

echo "[4/5] Atualizando privilégios..."
$MYSQL_CMD -e "FLUSH PRIVILEGES;"

echo "[5/5] Importando dados de teste do arquivo db_fluxocapital_sync.sql..."
if [ -f "db_fluxocapital_sync.sql" ]; then
    if $MYSQL_CMD -D db_fluxocapital < db_fluxocapital_sync.sql; then
        echo ""
        echo "✅ Banco de dados configurado e populado com sucesso!"
    else
        echo ""
        echo "❌ Erro ao importar os dados do arquivo .sql!"
        exit 1
    fi
else
    echo "❌ Erro: Arquivo db_fluxocapital_sync.sql não encontrado no diretório atual!"
    exit 1
fi
