# FluxoCapital
# 📊 Sistema de Gestão de Investimentos & Finanças

Este é um ecossistema completo de gestão financeira pessoal e de investimentos, desenvolvido com **Python** e **Flask**. O sistema foi desenhado para operar num ambiente híbrido, otimizando o desenvolvimento local e em servidores remotos Linux.

## 🏗️ Arquitetura do Projeto

O sistema utiliza uma arquitetura modular baseada em **Blueprints** do Flask para separar a lógica de investimentos da lógica de finanças pessoais.

### Componentes Principais:
- **`app.py`**: Ponto de entrada da aplicação, gestão de autenticação, rotas de ativos e integração de dividendos.
- **`finance.py`**: Módulo dedicado ao fluxo de caixa, gestão de despesas fixas, variáveis e relatórios detalhados.
- **`models.py`**: Definição do esquema da base de dados (MariaDB) utilizando SQLAlchemy.
- **`card_parser.py`**: Utilitário de automação que utiliza `pdfplumber` para extrair dados de faturas de cartão de crédito (ex: XP Investimentos).
- **`extensions.py`**: Centralização de extensões (DB, LoginManager) para evitar importações circulares.

## 🛠️ Funcionalidades Detalhadas

### 📈 Investimentos
- **Preço Médio e Yield on Cost (YoC)**: Cálculo automático baseado no histórico de compras.
- **Cotações em Tempo Real**: Integração via API para atualização de preços e P/VP (`update_prices.py`).
- **Relatórios**: Visão de aportes mensais e evolução de proventos.

### 💳 Finanças Pessoais
- **Importação de PDF**: Lançamento automático de gastos de cartão de crédito através da leitura da fatura.
- **Despesas Fixas**: Geração automática de contas recorrentes no início de cada mês.
- **Multicarteiras**: Separação de fluxos financeiros por perfil (ex: Pessoal vs. Família).

---

## 🔐 Segurança e Compliance

- **RBAC (Role-Based Access Control)**: Sistema de perfis de utilizador (Admin, Gestor, Familiar) para restrição de acesso a áreas sensíveis.
- **Logs de Auditoria**: Monitorização de acessos (`login_errors.log`) e ações de utilizador (`user_actions.log`).
- **Ambiente Isolado**: Dependências geridas via `venv` (Virtual Environment).

---

## 🚀 Como Iniciar

### Requisitos:
- Python 3.9+
- MariaDB / MySQL
- Dependências listadas em `requirements.txt`

### Configuração do Banco de Dados:
A aplicação vem com um banco de dados de testes em `db_fluxocapital_sync.sql`.
Crie um banco novo em seu MariaDB/MySQL local e importe a estrutura e os dados fictícios:
```bash
mysql -u root -p -e "CREATE DATABASE db_fluxocapital;"
mysql -u root -p db_fluxocapital < db_fluxocapital_sync.sql
```

Na sequência, crie um arquivo `.env` na raiz do projeto contendo as suas credenciais:
```ini
DB_USER=root
DB_PASS=sua_senha
DB_HOST=localhost
DB_NAME=db_fluxocapital
```

### Execução Local:
```bash
# Crie e ative seu ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instale as dependências
pip install --upgrade pip
pip install -r requirements.txt

# Execute a aplicação
python3 app.py
```