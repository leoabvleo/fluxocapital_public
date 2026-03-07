import os
from app import app
from extensions import db

def create_table():
    with app.app_context():
        try:
            db.create_all()
            print("Table `usuario_carteira` checked/created.")
        except Exception as e:
            print("Error creating table:", e)

if __name__ == '__main__':
    create_table()
