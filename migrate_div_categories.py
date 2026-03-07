import os
from app import app
from extensions import db
from models import Dividendo, Ativo
from sqlalchemy import text

def migrate():
    with app.app_context():
        try:
            # 1. Add the column using raw SQL if it doesn't exist
            print("Adding column categoria_id to dividendos table...")
            try:
                db.session.execute(text("ALTER TABLE dividendos ADD COLUMN categoria_id INT NULL"))
                db.session.execute(text("ALTER TABLE dividendos ADD CONSTRAINT fk_div_categoria_ativo FOREIGN KEY (categoria_id) REFERENCES categoria_ativos(id)"))
                db.session.commit()
                print("Column and FK added successfully.")
            except Exception as e:
                db.session.rollback()
                print(f"Column might already exist or error: {e}")

            # 2. Populate the column based on Ativo table if possible
            print("Populating categoria_id based on Ativo table...")
            dividendos = Dividendo.query.filter(Dividendo.categoria_id == None).all()
            updated_count = 0
            
            # Cache asset categories
            ticker_cat_map = {}
            
            for div in dividendos:
                if div.ticker in ticker_cat_map:
                    div.categoria_id = ticker_cat_map[div.ticker]
                    updated_count += 1
                else:
                    ativo = Ativo.query.filter_by(ticker=div.ticker).first()
                    if ativo and ativo.categoria_id:
                        div.categoria_id = ativo.categoria_id
                        ticker_cat_map[div.ticker] = ativo.categoria_id
                        updated_count += 1
            
            db.session.commit()
            print(f"Migration completed. {updated_count} records updated.")

        except Exception as e:
            db.session.rollback()
            print(f"General error during migration: {e}")

if __name__ == '__main__':
    migrate()
