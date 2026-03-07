#!/bin/bash
# Script: import-db-Mac2Oracle.sh (Oracle Cloud)
#02-03-2026

DB_NAME="db_fluxocapital"
DUMP_FILE="/home/ubuntu/db_fluxocapital_sync.sql.gz"

echo "==============================================="
echo "📥 IMPORTANDO BANCO (SYNC MACMINI -> CLOUD)"
echo "==============================================="

if [ -f "$DUMP_FILE" ]; then
    echo "🔍 Backup encontrado. Descomprimindo e importando..."
    
    # Descomprime e injeta direto no MySQL
	gunzip < $DUMP_FILE | mysql --default-character-set=utf8mb4 $DB_NAME

    if [ $? -eq 0 ]; then
        echo "✅ Banco de dados atualizado com sucesso!"
        # Opcional: rm $DUMP_FILE
    else
        echo "❌ ERRO: Falha na importação. Verifique o banco."
    fi
else
    echo "❌ ERRO: Arquivo $DUMP_FILE não encontrado."
fi
