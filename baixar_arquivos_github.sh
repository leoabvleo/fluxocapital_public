#!/bin/bash

# Configurações de caminho
TARGET="/var/www/fluxocapital"
# Detecta quem está rodando o script agora
USUARIO_ATUAL=$(whoami)

echo "==============================================="
echo "🚀 Baixando arquivos do Github: FluxoCapital"
echo "==============================================="

# 1. Navega até o diretório
if cd "$TARGET"; then
    echo "📂 Diretório atual: $(pwd) [Usuário: $USUARIO_ATUAL]"
else
    echo "❌ ERRO: Não foi possível acessar $TARGET"
    exit 1
fi

# 2. Ajusta o remote (Garante que está baixando do repositório correto)
echo "🔗 Configurando repositório FluxoCapital..."
git remote set-url origin https://github.com/leoabvleo/fluxocapital.git

# 3. Executa o Pull
echo "📥 Puxando atualizações do Git..."
if git pull origin main; then
    echo "✅ Git pull realizado com sucesso."
else
    echo "❌ ERRO: Falha no Git Pull. Verifique conflitos ou permissões."
    exit 1
fi

# 4. Ajuste de permissões dinâmico
echo "🔐 Ajustando permissões de proprietário..."

if [[ "$OSTYPE" == "darwin"* ]]; then
    # No Mac
    USER_GROUP="$USUARIO_ATUAL:staff"
    echo "🍎 macOS: Aplicando $USER_GROUP"
    chown -R $USER_GROUP "$TARGET"
else
    # No Linux (Produção ou Davinci)
    # Mantém você como dono e coloca o servidor web como grupo
    USER_GROUP="$USUARIO_ATUAL:www-data"
    echo "🐧 Linux: Aplicando $USER_GROUP"
    sudo chown -R $USER_GROUP "$TARGET"
    sudo chmod -R 775 "$TARGET"
fi

# 5. Reinicialização dos serviços (Estratégia Minimalista)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "💡 Flask em modo Debug no Mac reiniciará sozinho."
else
    # Em vez de restartar o Apache todo, apenas dá um 'refresh' no app Python
    echo "🔄 Notificando aplicação (WSGI Touch)..."
    touch "$TARGET"/*.wsgi
    
    # Se ainda assim quiser o restart do Apache, mantive aqui:
    # sudo systemctl restart apache2 && echo "✅ Apache reiniciado!"
fi

echo "======================================"
echo "🎉 Processo concluído com sucesso!"
