import os
from app import app
from extensions import db
from models import Dividendo, CategoriaAtivo
from sqlalchemy import text

def migrate():
    with app.app_context():
        try:
            print("Updating categoria_id in dividendos table based on manual list...")
            
            # Get IDs for categories
            acoes = CategoriaAtivo.query.filter_by(nome='Ações').first()
            renda_fixa = CategoriaAtivo.query.filter_by(nome='Renda Fixa').first()
            
            if not acoes or not renda_fixa:
                print(f"Error: Categories not found. Ações: {acoes}, Renda Fixa: {renda_fixa}")
                return

            # Tickers for Ações
            tickers_acoes = ['ENGI3', 'EQTL3', 'JBSS3', 'PETR4', 'STBP3', 'TRPL4', 'VALE3', 'WEGE3']
            # Tickers for Renda Fixa
            tickers_rf = [
                'Prefixado Juros 2029 Odília', 
                'Mercado Pago Leo - Rendimentos', 
                'Mercado Pago Odilia - Rendimentos', 
                'XP INVESTBACK'
            ]

            # Update Ações
            updated_acoes = Dividendo.query.filter(Dividendo.ticker.in_(tickers_acoes)).update(
                {Dividendo.categoria_id: acoes.id}, synchronize_session=False
            )
            print(f"Updated {updated_acoes} records to 'Ações'.")

            # Update Renda Fixa
            updated_rf = Dividendo.query.filter(Dividendo.ticker.in_(tickers_rf)).update(
                {Dividendo.categoria_id: renda_fixa.id}, synchronize_session=False
            )
            print(f"Updated {updated_rf} records to 'Renda Fixa'.")
            
            db.session.commit()
            print("Migration completed successfully.")

        except Exception as e:
            db.session.rollback()
            print(f"General error during migration: {e}")

if __name__ == '__main__':
    migrate()
