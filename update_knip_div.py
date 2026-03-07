import os
from app import app
from extensions import db
from models import Dividendo, CategoriaAtivo
from sqlalchemy import text

def migrate():
    with app.app_context():
        try:
            print("Updating categoria_id for KNIP11 in dividendos table to FIIs...")
            
            # Get ID for FIIs category
            fiis = CategoriaAtivo.query.filter_by(nome='FIIs').first()
            
            if not fiis:
                print("Error: 'FIIs' category not found.")
                return

            # Update KNIP11
            updated_count = Dividendo.query.filter_by(ticker='KNIP11').update(
                {Dividendo.categoria_id: fiis.id}, synchronize_session=False
            )
            print(f"Updated {updated_count} records for KNIP11 to 'FIIs'.")
            
            db.session.commit()
            print("Migration completed successfully.")

        except Exception as e:
            db.session.rollback()
            print(f"General error during migration: {e}")

if __name__ == '__main__':
    migrate()
