#!/bin/bash
# Script: exportar-db-Oracle2Mac.sh
# Utilidade: Gerar backup do banco de dados no servidor de produção

DB_NAME="db_fluxocapital"
DB_USER="user_fluxocapital"
DB_PASS="1qhnTXZDCz8P4cB7n"

# Configurações de Caminho
BASE_DIR="/var/www/fluxocapital"
BACKUP_DIR="/home/ubuntu"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DUMP_NAME="db_fluxocapital_prod_$TIMESTAMP.sql.gz"

echo "==============================================="
echo "💾 GERANDO BACKUP DO BANCO NO SERVIDOR"
echo "==============================================="

# 1. Garantir que o diretório de backup existe
if [ ! -d "$BACKUP_DIR" ]; then
    echo "📂 Criando diretório de backup em $BACKUP_DIR..."
    mkdir -p "$BACKUP_DIR"
fi

cd "$BASE_DIR" || exit 1

echo "📡 Gerando dump e comprimindo..."
# 'sed' remove comentário de sandbox do MariaDB 11+ para evitar erro em versões antigas
if mysqldump --default-character-set=utf8mb4 -u $DB_USER -p$DB_PASS $DB_NAME | sed '/sandbox mode/d' | gzip > "$BACKUP_DIR/$DUMP_NAME"; then
    echo "✅ Backup gerado com sucesso: $BACKUP_DIR/$DUMP_NAME"
    # Ajusta permissão para o usuário ubuntu (necessário se rodar como root)
    chown ubuntu:ubuntu "$BACKUP_DIR/$DUMP_NAME" 2>/dev/null
else
    echo "❌ ERRO: Falha ao gerar o dump do MySQL."
    exit 1
fi

# 2. Rotação de Backups: Manter apenas os últimos 7
echo "🧹 Limpando backups antigos (mantendo os últimos 7)..."
ls -t "$BACKUP_DIR"/db_fluxocapital_prod_*.sql.gz | tail -n +8 | xargs rm -f

echo "==============================================="
echo "🎉 Processo concluído com sucesso!"
