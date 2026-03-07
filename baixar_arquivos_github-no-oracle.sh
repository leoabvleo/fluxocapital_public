#!/bin/bash
# Script: baixar_arquivos_github-no-oracle.sh (Versão FluxoCapital)

echo "==============================================="
echo "🚀 Baixando atualizações do Github: FluxoCapital"
echo "==============================================="

# 1. Ajusta o remote (Garante que está baixando do repositório correto)
echo "🔗 Configurando repositório FluxoCapital..."
git remote set-url origin https://github.com/leoabvleo/fluxocapital.git

# 2. Guarda mudanças locais temporárias (Evita conflitos no pull)
echo "📦 Guardando alterações locais (Stash)..."
git stash

# 3. Puxa as atualizações
echo "📥 Puxando novidades do repositório..."
if git pull origin main; then
    echo "✅ Git pull realizado com sucesso."
else
    echo "❌ ERRO: Falha no Git Pull. Verifique a conexão ou se houve conflito."
    exit 1
fi

# 4. Tenta devolver mudanças locais (Se houver stash)
# git stash pop

# 5. Roda as migrações automaticamente
echo "⚙️ Verificando ambiente virtual e migrações..."
if [ -d "venv" ]; then
    source venv/bin/activate
    # Caso precise rodar migrações específicas:
    # python3 migrate_add_posicao.py
fi

echo "🔐 Ajustando permissões de sistema (www-data)..."
sudo chown -R $USER:www-data .
sudo chmod -R 775 .

echo "🔄 Reiniciando aplicação (WSGI Touch)..."
touch adapter.wsgi

echo "🎉 Processo concluído com sucesso!"
