#!/bin/bash
# Script: exportar-db-Mac para Oracle.sh (MacMini)

DB_NAME="db_fluxocapital"
DB_USER="user_fluxocapital"
DB_PASS="1qhnTXZDCz8P4cB7n"
DUMP_NAME="db_fluxocapital_sync.sql.gz"
TARGET_DIR="/private/var/www/fluxocapital"

echo "==============================================="
echo "📤 SINCRONIZANDO BANCO PARA PRODUÇÃO"
echo "==============================================="

cd $TARGET_DIR

echo "📡 Gerando dump e comprimindo..."
# Usando a senha diretamente para facilitar a automação
# Adicionado 'sed' para remover comentário de sandbox do MariaDB 11+ que quebra em versões antigas

if mysqldump --default-character-set=utf8mb4 -u $DB_USER -p$DB_PASS $DB_NAME | \
   sed '/sandbox mode/d' | \
   sed 's/CONSTRAINT `[^`]*` FOREIGN KEY/FOREIGN KEY/g' | \
   gzip > $DUMP_NAME; then

#if mysqldump --default-character-set=utf8mb4 -u $DB_USER -p$DB_PASS $DB_NAME | sed '/sandbox mode/d' | gzip > $DUMP_NAME; then
    echo "✅ Dump gerado com sucesso!"
else
    echo "❌ ERRO: Falha ao gerar o dump do MySQL."
    exit 1
fi

echo "🚚 Enviando via SCP para a Nuvem..."
if scp $DUMP_NAME oracle:/home/ubuntu/; then
    echo "✅ Arquivo enviado com sucesso!"
    rm $DUMP_NAME
    echo "💡 Agora acesse o servidor Oracle e rode o script de importação."
else
    echo "❌ ERRO: Falha ao enviar o arquivo via SCP."
    exit 1
fi
