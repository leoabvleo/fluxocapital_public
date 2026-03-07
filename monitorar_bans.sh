#!/bin/bash

# Cores para facilitar a leitura
VERMELHO='\033[0;31m'
VERDE='\033[0;32m'
AZUL='\033[0;34m'
NC='\033[0m' # Sem cor

echo -e "${AZUL}====================================================${NC}"
echo -e "${AZUL}      RELATÓRIO DE SEGURANÇA - FAIL2BAN             ${NC}"
echo -e "${AZUL}====================================================${NC}"

# 1. Lista Jails Ativas
echo -e "\n${VERDE}[+] Jails Ativas no Fail2Ban:${NC}"
fail2ban-client status | grep "Jail list" | sed 's/`- Jail list://'

# 2. Resumo de IPs bloqueados via IPTABLES
echo -e "\n${VERDE}[+] IPs Bloqueados Atualmente (Iptables):${NC}"

# Extrai IPs das chains que começam com f2b- ou fail2ban-
chains=$(iptables -L -n | grep -E "Chain (f2b|fail2ban)" | awk '{print $2}')

for chain in $chains; do
    count=$(iptables -L $chain -n | grep "REJECT" | wc -l)
    if [ $count -gt 0 ]; then
        echo -e "${AZUL}Chain: $chain ($count IPs)${NC}"
        iptables -L $chain -n | grep "REJECT" | awk '{print "  - " $4}'
    fi
done

# 3. Tentativas de hoje nos Logs
echo -e "\n${VERDE}[+] Bloqueios registrados hoje no log:${NC}"
log_file="/var/log/fail2ban.log"
if [ -f "$log_file" ]; then
    today=$(date "+%Y-%m-%d")
    grep "$today" "$log_file" | grep "Ban" | awk '{print "  ["$1" "$2"] " $NF " banido na jail "$7}'
else
    echo "  Arquivo de log não encontrado em $log_file"
fi

echo -e "\n${AZUL}====================================================${NC}"
