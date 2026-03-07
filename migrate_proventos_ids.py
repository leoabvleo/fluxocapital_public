import os
from app import app
from extensions import db
from models import Dividendo, CategoriaProvento
from sqlalchemy import text

def migrate():
    with app.app_context():
        try:
            # 1. Add the column using raw SQL if it doesn't exist
            # Note: For MariaDB/MySQL
            print("Adding column categoria_provento_id to dividendos table...")
            try:
                db.session.execute(text("ALTER TABLE dividendos ADD COLUMN categoria_provento_id INT NULL"))
                db.session.execute(text("ALTER TABLE dividendos ADD CONSTRAINT fk_categoria_provento FOREIGN KEY (categoria_provento_id) REFERENCES categoria_proventos(id)"))
                db.session.commit()
                print("Column and FK added successfully.")
            except Exception as e:
                db.session.rollback()
                print(f"Column might already exist or error: {e}")

            # 2. Populate the column based on 'tipo'
            print("Populating categoria_provento_id based on tipo...")
            categorias = CategoriaProvento.query.all()
            cat_map = {cat.nome: cat.id for cat in categorias}

            dividendos = Dividendo.query.all()
            updated_count = 0
            for div in dividendos:
                if div.tipo in cat_map:
                    div.categoria_provento_id = cat_map[div.tipo]
                    updated_count += 1
                else:
                    # Optional: Handle cases where 'tipo' doesn't match any category
                    # Maybe map to 'Dividendos' as default if it exists
                    if 'Dividendos' in cat_map:
                        div.categoria_provento_id = cat_map['Dividendos']
                        updated_count += 1
            
            db.session.commit()
            print(f"Migration completed. {updated_count} records updated.")

        except Exception as e:
            db.session.rollback()
            print(f"General error during migration: {e}")

if __name__ == '__main__':
    migrate()
