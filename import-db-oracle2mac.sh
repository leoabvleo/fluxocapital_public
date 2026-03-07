#!/bin/bash
# Script: import-db-oracle2mac.sh
# Utilidade: Baixar o último backup do servidor Oracle e importar no banco local (Mac)

DB_NAME="db_fluxocapital"
DB_USER="user_fluxocapital"
DB_PASS="1qhnTXZDCz8P4cB7n"

echo "==============================================="
echo "📥 IMPORTANDO BANCO (PRODUÇÃO -> MACMINI)"
echo "==============================================="

# 1. Identificar o backup mais recente no servidor Oracle via SSH
echo "🔍 Buscando backup mais recente no servidor Oracle..."
LATEST_BACKUP=$(ssh oracle "ls -t /home/ubuntu/db_fluxocapital_sync.sql.gz>/dev/null | head -n 1")


if [ -z "$LATEST_BACKUP" ]; then
    echo "❌ ERRO: Nenhum backup encontrado em oracle:/home/ubuntu/"
    exit 1
fi

FILE_NAME=$(basename "$LATEST_BACKUP")
echo "📦 Backup encontrado: $FILE_NAME"

# 2. Baixar o arquivo via SCP
echo "🚚 Baixando arquivo para o Mac..."
if scp oracle:"$LATEST_BACKUP" .; then
#if scp ubuntu@144.22.239.218:"$LATEST_BACKUP" .; then
    echo "✅ Download concluído!"
else
    echo "❌ ERRO: Falha ao baixar o arquivo via SCP."
    exit 1
fi

# 3. Importar no banco de dados local
echo "💉 Importando para o MariaDB local ($DB_NAME)..."
if [ -f "$FILE_NAME" ]; then
    # Descomprime e injeta direto no MySQL/MariaDB
    if gunzip < "$FILE_NAME" | mysql -u $DB_USER -p$DB_PASS $DB_NAME; then
        echo "✅ Importação concluída com sucesso!"
        
        # 4. Limpeza
        echo "🧹 Removendo arquivo local $FILE_NAME..."
        rm "$FILE_NAME"
    else
        echo "❌ ERRO: Falha na importação do dump."
        exit 1
    fi
else
    echo "❌ ERRO: Arquivo $FILE_NAME não encontrado localmente."
    exit 1
fi

echo "==============================================="
echo "🎉 Processo finalizado!"
