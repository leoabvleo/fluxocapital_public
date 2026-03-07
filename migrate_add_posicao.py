from app import app
from extensions import db
from sqlalchemy import text

def migrate():
    with app.app_context():
        # Adiciona coluna posicao na tabela transacoes
        try:
            db.session.execute(text('ALTER TABLE transacoes ADD COLUMN posicao INTEGER DEFAULT 0'))
            print("Coluna 'posicao' adicionada em 'transacoes'")
        except Exception as e:
            print(f"Erro ao adicionar 'posicao' em 'transacoes': {e}")

        # Adiciona coluna posicao na tabela config_financeiras_fixas
        try:
            db.session.execute(text('ALTER TABLE config_financeiras_fixas ADD COLUMN posicao INTEGER DEFAULT 0'))
            print("Coluna 'posicao' adicionada em 'config_financeiras_fixas'")
        except Exception as e:
            print(f"Erro ao adicionar 'posicao' em 'config_financeiras_fixas': {e}")

        db.session.commit()

if __name__ == "__main__":
    migrate()
