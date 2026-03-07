from app import app, db
from sqlalchemy import text

def run_migration():
    with app.app_context():
        print("Iniciando migração para adicionar folha_id em funcionario_lancamentos...")
        try:
            # MariaDB / MySQL syntax
            db.session.execute(text("ALTER TABLE funcionario_lancamentos ADD COLUMN folha_id INT DEFAULT NULL"))
            db.session.execute(text("ALTER TABLE funcionario_lancamentos ADD CONSTRAINT fk_folha_id FOREIGN KEY (folha_id) REFERENCES folha_pagamentos(id)"))
            db.session.commit()
            print("✓ Coluna folha_id e constraint de chave estrangeira adicionadas!")
        except Exception as e:
            db.session.rollback()
            # Se a coluna já existir, ignora o erro
            if "Duplicate column name" in str(e):
                print("! Coluna folha_id já existe. Pulando...")
            else:
                print(f"✗ Erro durante a migração: {e}")

if __name__ == "__main__":
    run_migration()
