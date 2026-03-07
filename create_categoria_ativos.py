import os
from app import app
from extensions import db
from models import CategoriaAtivo

def create_and_populate():
    with app.app_context():
        try:
            # Create the table if it doesn't exist
            db.create_all()
            print("Tables checked/created.")

            # Initial data
            categorias = [
                "Ações",
                "FIIs",
                "ETFs",
                "BDRs",
                "Internacional",
                "Renda Fixa",
                "Previdência",
                "Cripto"
            ]

            for nome in categorias:
                exists = CategoriaAtivo.query.filter_by(nome=nome).first()
                if not exists:
                    nova_categoria = CategoriaAtivo(nome=nome)
                    db.session.add(nova_categoria)
                    print(f"Added category: {nome}")
                else:
                    print(f"Category already exists: {nome}")
            
            db.session.commit()
            print("Population successful.")
        except Exception as e:
            db.session.rollback()
            print("Error:", e)

if __name__ == '__main__':
    create_and_populate()
