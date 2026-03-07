"""
Migração: adiciona coluna carteira_id na tabela funcionarios
e vincula os registros existentes à carteira id=6 (Laelson).
Execute: python migrate_funcionarios_carteira.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from sqlalchemy import text

with app.app_context():
    with db.engine.connect() as conn:
        # 1. Adiciona a coluna (ignora se já existir)
        try:
            conn.execute(text("ALTER TABLE funcionarios ADD COLUMN carteira_id INTEGER REFERENCES carteiras(id)"))
            conn.commit()
            print("✓ Coluna carteira_id adicionada à tabela funcionarios.")
        except Exception as e:
            if 'duplicate column' in str(e).lower() or 'already exists' in str(e).lower():
                print("ℹ Coluna carteira_id já existe — pulando ALTER TABLE.")
            else:
                raise e

        # 2. Vincula todos os registros existentes (sem carteira) à carteira id=6 (Laelson)
        result = conn.execute(
            text("UPDATE funcionarios SET carteira_id = 6 WHERE carteira_id IS NULL")
        )
        conn.commit()
        print(f"✓ {result.rowcount} funcionário(s) vinculado(s) à carteira Laelson (id=6).")

    print("Migração concluída!")
