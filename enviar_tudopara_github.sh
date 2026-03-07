#!/bin/bash

# 1. Ajusta o remote (Garante que está enviando para o repositório correto)
echo "🔗 Configurando repositório FluxoCapital..."
git remote set-url origin git@github.com:leoabvleo/fluxocapital.git

# 2. Ajusta a branch para 'main' (Resolve o erro 'src refspec main does not match')
git branch -M main

# 3. Adiciona as alterações
echo "➕ Adicionando arquivos..."
git add .

# 4. Commit com data e hora automática
MSG="Update automático: $(date +'%d/%m/%Y %H:%M')"
echo "💾 Criando commit: $MSG"
git commit -m "$MSG"

# 5. Envia para o GitHub
echo "🚀 Enviando para o repositório FluxoCapital..."
if git push origin main; then
    echo "✅ Sucesso! Código enviado para github.com/leoabvleo/fluxocapital"
else
    echo "❌ ERRO: Falha no push. Verifique o token ou a conexão."
    exit 1
fi
