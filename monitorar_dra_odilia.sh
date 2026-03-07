#!/bin/bash
# monitorar_dra_odilia.sh

ROOT_DIR="/var/www/fluxocapital"
HIST_FILE="$ROOT_DIR/history_fluxocapital.log"
DATE_LOG=$(date '+%Y-%m-%d')

# 1. Coleta total de hoje no log do Fail2Ban
TOTAL_HOJE=$(grep "$DATE_LOG" /var/log/fail2ban.log | grep "Ban" | wc -l)

# 2. Atualiza arquivo de histórico
if grep -q "$DATE_LOG" "$HIST_FILE" 2>/dev/null; then
    sed -i "/$DATE_LOG/c\\$DATE_LOG | $TOTAL_HOJE" "$HIST_FILE"
else
    echo "$DATE_LOG | $TOTAL_HOJE" >> "$HIST_FILE"
fi
tail -n 10 "$HIST_FILE" > "${HIST_FILE}.tmp" && mv "${HIST_FILE}.tmp" "$HIST_FILE"

# 3. Calcula Somatório 10 dias
SOMA_10=0
while read -r line; do
    valor=$(echo "$line" | awk -F'|' '{print $2}' | xargs)
    SOMA_10=$((SOMA_10 + valor))
done < "$HIST_FILE"

# 4. Exibe na tela com as cores que você gosta
AZUL='\033[0;34m'
VERDE='\033[0;32m'
NC='\033[0m'

echo -e "${AZUL}HISTÓRICO DE ATAQUES - SISTEMA DRA. ODÍLIA${NC}"
cat "$HIST_FILE"
echo -e "${VERDE}---------------------------------------${NC}"
echo -e "${VERDE}TOTAL DE BLOQUEIOS NOS ÚLTIMOS 10 DIAS: $SOMA_10${NC}"
