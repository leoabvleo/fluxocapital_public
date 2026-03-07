#!/bin/bash

# =================================================================
# SCRIPT: gerar-painel-bloqueios.sh (SOC Pessoal)
# Desenvolvido por: Leonardo Americo
# =================================================================

# Configurações de Caminho
ROOT_DIR="/var/www/fluxocapital"
HIST_FILE="$ROOT_DIR/history_fluxocapital.log"
HTML_FILE="/var/www/draodiliaoftalmo.com.br/seguranca.html"
DATE_LOG=$(date '+%Y-%m-%d')
NOW=$(date '+%d/%m/%Y %H:%M:%S')

# Função para Geolocalização via API
get_geo() {
    local ip=$1
    if [ -z "$ip" ]; then echo "N/A"; return; fi
    curl -s --max-time 2 "http://ip-api.com/line/$ip?fields=status,countryCode,city" | tr '\n' ' ' | sed 's/success //'
}

# 1. Coleta de Dados do Fail2Ban e Somatório Atual
JAILS=$(fail2ban-client status | grep "Jail list" | sed 's/.*Jail list://' | sed 's/,//g')

SOMA_ATUAL=0
for jail in $JAILS; do
    # Conta quantos IPs existem na lista de cada jail
    count=$(fail2ban-client status $jail | grep "Currently banned" | awk '{print $NF}')
    SOMA_ATUAL=$((SOMA_ATUAL + count))
done

# 2. Total Acumulado do Dia (Logs)
TOTAL_HOJE=$(grep "$DATE_LOG" /var/log/fail2ban.log | grep "Ban" | wc -l)

# 3. Atualização do Histórico e Somatório de 10 dias
if grep -q "$DATE_LOG" "$HIST_FILE" 2>/dev/null; then
    sed -i "/$DATE_LOG/c\\$DATE_LOG | $TOTAL_HOJE" "$HIST_FILE"
else
    echo "$DATE_LOG | $TOTAL_HOJE" >> "$HIST_FILE"
fi
tail -n 10 "$HIST_FILE" > "${HIST_FILE}.tmp" && mv "${HIST_FILE}.tmp" "$HIST_FILE"

SOMA_10=0
while read -r line; do
    valor=$(echo "$line" | awk -F'|' '{print $2}' | xargs)
    SOMA_10=$((SOMA_10 + valor))
done < "$HIST_FILE"

# --- GERAÇÃO DO HTML ---
cat <<EOF > $HTML_FILE
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8"><meta http-equiv="refresh" content="300">
    <title>SOC Pessoal - Leonardo Americo</title>
    <style>
        :root { --bg: #f4f7f6; --card: #ffffff; --blue: #00457d; --red: #dc3545; --green: #28a745; --border: #dee2e6; }
        body { font-family: 'Segoe UI', Tahoma, sans-serif; background: var(--bg); margin: 0; padding: 20px; color: #333; }
        .container { max-width: 1000px; margin: auto; }
        .header { background: var(--blue); color: #fff; padding: 20px; border-radius: 8px 8px 0 0; display: flex; justify-content: space-between; align-items: center; }
        .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0; }
        .stat-card { background: var(--card); padding: 15px; border-radius: 8px; text-align: center; border: 1px solid var(--border); box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .stat-card big { font-size: 30px; font-weight: bold; display: block; margin: 5px 0; }
        .main-grid { display: grid; grid-template-columns: 1fr 1.5fr; gap: 20px; }
        .block { background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 20px; }
        h2 { color: var(--blue); border-bottom: 2px solid #eee; padding-bottom: 10px; margin-top: 0; font-size: 18px; }
        table { width: 100%; border-collapse: collapse; font-size: 13px; }
        th { text-align: left; background: #f8f9fa; padding: 10px; border-bottom: 2px solid var(--border); }
        td { padding: 8px 10px; border-bottom: 1px solid #f1f1f1; }
        .ip-badge { background: #f8f9fa; border: 1px solid var(--border); padding: 6px 10px; border-radius: 4px; font-family: monospace; display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 12px; }
        .total-row { background: #e7f3ff; font-weight: bold; }
        .footer { text-align: center; color: #999; font-size: 11px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1 style="margin:0; font-size:22px;">Painel de Segurança - Leonardo Americo</h1>
                <span style="font-size:12px; opacity:0.8;">Monitoramento: Wordpress & Financeiro</span>
            </div>
            <div style="text-align:right; font-size:12px;">Gerado em: $NOW</div>
        </div>

        <div class="stats-grid">
            <div class="stat-card" style="border-top: 5px solid var(--green);">
                <span style="font-size:10px; font-weight:bold; color:#666; text-transform:uppercase;">Bans Hoje</span>
                <big style="color:var(--green)">$TOTAL_HOJE</big>
            </div>
            <div class="stat-card" style="border-top: 5px solid var(--red);">
                <span style="font-size:10px; font-weight:bold; color:#666; text-transform:uppercase;">Ativos Agora</span>
                <big style="color:var(--red)">$SOMA_ATUAL</big>
            </div>
            <div class="stat-card" style="border-top: 5px solid var(--blue);">
                <span style="font-size:10px; font-weight:bold; color:#666; text-transform:uppercase;">Total (10 dias)</span>
                <big style="color:var(--blue)">$SOMA_10</big>
            </div>
            <div class="stat-card" style="border-top: 5px solid #6c757d;">
                <span style="font-size:10px; font-weight:bold; color:#666; text-transform:uppercase;">Jails</span>
                <big style="color:#6c757d">$(echo $JAILS | wc -w)</big>
            </div>
        </div>

        <div class="main-grid">
            <div class="block">
                <h2>📅 Histórico Recente</h2>
                <table>
                    <thead><tr><th>Data</th><th style="text-align:right">Bans</th></tr></thead>
                    <tbody>
EOF

tac "$HIST_FILE" | while read -r line; do
    IFS='|' read -r d t <<< "$line"
    echo "<tr><td>$d</td><td style='text-align:right'><strong>$t</strong></td></tr>" >> $HTML_FILE
done

echo "<tr class='total-row'><td>TOTAL (10 DIAS)</td><td style='text-align:right'>$SOMA_10</td></tr>" >> $HTML_FILE

cat <<EOF >> $HTML_FILE
                    </tbody>
                </table>
            </div>

            <div class="block">
                <h2>🚫 IPs Bloqueados Atualmente ($SOMA_ATUAL)</h2>
EOF

for jail in $JAILS; do
    ips=$(fail2ban-client status $jail | grep "IP list" | sed 's/.*IP list://')
    if [ ! -z "$ips" ]; then
        echo "<h3 style='font-size:14px; color:var(--blue); margin: 15px 0 8px 0;'>Jail: $jail</h3>" >> $HTML_FILE
        for ip in $ips; do
            geo=$(get_geo $ip)
            echo "<div class='ip-badge'><span>$ip</span><span style='color:#888; font-size:10px;'>$geo</span></div>" >> $HTML_FILE
        done
    fi
done

cat <<EOF >> $HTML_FILE
            </div>
        </div>
        <div class="footer">
            SOC Pessoal Leonardo Americo • Proteção Wordpress & Sistemas Financeiros
        </div>
    </div>
</body></html>
EOF

chmod 644 $HTML_FILE
