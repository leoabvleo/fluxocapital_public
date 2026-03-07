import os
from app import app
from extensions import db
from models import Venda, CategoriaAtivo
from sqlalchemy import text

def migrate():
    with app.app_context():
        try:
            # 1. Add the column using raw SQL if it doesn't exist
            print("Adding column categoria_id to vendas table...")
            try:
                db.session.execute(text("ALTER TABLE vendas ADD COLUMN categoria_id INT NULL"))
                db.session.execute(text("ALTER TABLE vendas ADD CONSTRAINT fk_vendas_categoria_ativo FOREIGN KEY (categoria_id) REFERENCES categoria_ativos(id)"))
                db.session.commit()
                print("Column and FK added successfully.")
            except Exception as e:
                db.session.rollback()
                print(f"Column might already exist or error: {e}")

            # 2. Populate the column based on user rules
            print("Populating categoria_id based on user rules...")
            
            # Get IDs for categories
            renda_fixa = CategoriaAtivo.query.filter_by(nome='Renda Fixa').first()
            fiis = CategoriaAtivo.query.filter_by(nome='FIIs').first()
            acoes = CategoriaAtivo.query.filter_by(nome='Ações').first()
            
            if not acoes:
                print("Error: 'Ações' category not found.")
                return

            vendas = Venda.query.all()
            updated_count = 0
            
            for v in vendas:
                if v.ticker == 'IPCA+ 2045 - Leo (3,82%)' and renda_fixa:
                    v.categoria_id = renda_fixa.id
                elif v.ticker == 'KNIP11' and fiis:
                    v.categoria_id = fiis.id
                else:
                    v.categoria_id = acoes.id
                updated_count += 1
            
            db.session.commit()
            print(f"Migration completed. {updated_count} records updated.")

        except Exception as e:
            db.session.rollback()
            print(f"General error during migration: {e}")

if __name__ == '__main__':
    migrate()
