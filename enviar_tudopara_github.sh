#!/bin/bash

# --- CONFIGURAÇÕES DE AMBIENTE ---
# Caso não tenha configurado globalmente, o Git precisa saber quem você é
git config --global user.email "seu-email@exemplo.com"
git config --global user.name "Leo"

# --- 1. VERIFICAÇÃO DE REPOSITÓRIO ---
if [ ! -d ".git" ]; then
    echo "📂 Inicializando repositório Git em $(pwd)..."
    git init
    git remote add origin git@github.com:leoabvleo/fluxocapital.git
else
    echo "🔗 Atualizando URL do repositório remoto..."
    git remote set-url origin git@github.com:leoabvleo/fluxocapital.git
fi

# --- 2. PROTEÇÃO (OPCIONAL MAS RECOMENDADO) ---
# Impede que a pasta venv seja enviada (economiza tempo e evita erros)
if [ ! -f ".gitignore" ]; then
    echo "venv/" > .gitignore
    echo "index.php" >> .gitignore # Adicione outros se precisar
    echo "📝 Arquivo .gitignore criado."
fi

# --- 3. PREPARAÇÃO DA BRANCH ---
# Garante que estamos na 'main'
git branch -M main

# --- 4. ADIÇÃO E COMMIT ---
echo "➕ Adicionando arquivos..."
git add .

# Verifica se há algo para commitar (evita erro de 'nothing to commit')
if git diff-index --quiet HEAD --; then
    echo "ℹ️ Nenhuma alteração detectada para commit."
else
    MSG="Update automático: $(date +'%d/%m/%Y %H:%M')"
    echo "💾 Criando commit: $MSG"
    git commit -m "$MSG"
fi

# --- 5. ENVIO AO GITHUB ---
echo "🚀 Enviando para o GitHub (branch main)..."

# Usamos -u na primeira vez para vincular as branches
if git push -u origin main; then
    echo "✅ Sucesso! Código enviado para github.com/leoabvleo/fluxocapital"
else
    echo "❌ ERRO: Falha no push."
    echo "DICA: Verifique se sua chave SSH está adicionada ao GitHub com: ssh -T git@github.com"
    exit 1
fi
