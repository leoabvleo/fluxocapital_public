#!/bin/bash

# --- 1. IDENTIFICAÇÃO ---
HOSTNAME=$(hostname)
OS_TYPE="$OSTYPE"

echo "==============================================="
echo "🖥️  Ambiente Detectado: $HOSTNAME"

# Configuração de Caminhos e Modos
if [[ "$HOSTNAME" == "webserver.draodiliaoftalmo.com.br" ]]; then
    MODE="PRODUÇÃO (Oracle Cloud)"
    PUSH_PARAMS="--force"
    TARGET_DIR="/var/www/fluxocapital"
elif [[ "$HOSTNAME" == "Mac-Mini-M4.local" ]]; then
    MODE="DESENVOLVIMENTO (Mac Mini)"
    PUSH_PARAMS="" 
    TARGET_DIR="/var/www/fluxocapital"
elif [[ "$HOSTNAME" == "davinci" ]]; then
    MODE="TRABALHO (Davinci)"
    PUSH_PARAMS=""
    TARGET_DIR="$(pwd)"
else
    MODE="GENÉRICO"
    PUSH_PARAMS=""
    TARGET_DIR="$(pwd)"
fi

echo "🚀 Modo: $MODE"
echo "==============================================="

# --- 2. GARANTIR .GITIGNORE (Limpeza do Repo) ---
# Adicionei os logs e sql que vi no seu ls -lh
if [ ! -f ".gitignore" ]; then
    echo "venv/
__pycache__/
*.log
*.sql.gz
*.xlsx
.DS_Store" > .gitignore
    echo "📝 .gitignore atualizado para ignorar logs e dumps."
fi

# --- 3. AÇÃO: DOWNLOAD OU UPLOAD ---
if [ "$1" == "download" ]; then
    echo "📥 Sincronizando: GitHub -> Local..."
    git fetch origin main
    if git reset --hard origin/main; then
        echo "✅ Reset Local concluído (Igual ao GitHub)."
    else
        echo "❌ Falha na sincronização."
        exit 1
    fi
else
    echo "📤 Sincronizando: Local -> GitHub..."
    
    # Remove venv e logs do rastreio se existirem
    git rm -r --cached venv/ *.log 2>/dev/null
    
    git add .
    
    if git diff-index --quiet HEAD --; then
        echo "ℹ️  Nada novo para subir."
    else
        MSG="Sync automático [$MODE]: $(date +'%d/%m/%Y %H:%M')"
        git commit -m "$MSG"
    fi

    if git push origin main $PUSH_PARAMS; then
        echo "✅ Sucesso! Código no ar."
    else
        echo "⚠️  ERRO: PUSH REJEITADO."
        echo "💡 Use './git_sync.sh download' para igualar as versões primeiro."
        exit 1
    fi
fi

# --- 4. REGRAS DE PERMISSÃO (Apenas Oracle) ---
if [[ "$HOSTNAME" == *"webserver"* ]]; then
    echo "🔐 Aplicando permissões de Produção (www-data)..."
    chown -R root:www-data "$TARGET_DIR"
    chmod -R 775 "$TARGET_DIR"
    # Notifica o servidor Python (WSGI)
    touch "$TARGET_DIR/adapter.wsgi" 2>/dev/null
fi
