import os
from app import app
from extensions import db
from sqlalchemy import text
from models import CategoriaAtivo, Ativo

def migrate():
    with app.app_context():
        try:
            # 1. Add categoria_id column to ativos table
            print("Adding categoria_id column to ativos table...")
            db.session.execute(text("ALTER TABLE ativos ADD COLUMN categoria_id INT NULL"))
            db.session.execute(text("ALTER TABLE ativos ADD CONSTRAINT fk_ativo_categoria_ativo FOREIGN KEY (categoria_id) REFERENCES categoria_ativos(id)"))
            db.session.commit()
            print("Column and FK added.")
        except Exception as e:
            print(f"Column might already exist: {e}")
            db.session.rollback()

        try:
            # 2. Map existing string categories to IDs
            print("Mapping existing categories to IDs...")
            ativos = Ativo.query.all()
            categorias_db = {c.nome: c.id for c in CategoriaAtivo.query.all()}
            
            for a in ativos:
                if a.categoria in categorias_db:
                    a.categoria_id = categorias_db[a.categoria]
                else:
                    # If category doesn't exist, maybe create it or assign to a default?
                    # For now, let's just print a warning.
                    print(f"Warning: Category '{a.categoria}' not found in categoria_ativos for asset {a.ticker}")
            
            db.session.commit()
            print("Migration of data completed.")
        except Exception as e:
            print(f"Error migrating data: {e}")
            db.session.rollback()

if __name__ == '__main__':
    migrate()
