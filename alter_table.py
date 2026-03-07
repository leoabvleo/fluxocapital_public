import os
from app import app
from extensions import db
from sqlalchemy import text

def alter_table():
    with app.app_context():
        try:
            db.session.execute(text("ALTER TABLE gastos_cartao ADD COLUMN categoria_id INT NULL"))
            db.session.execute(text("ALTER TABLE gastos_cartao ADD CONSTRAINT fk_gasto_categoria FOREIGN KEY (categoria_id) REFERENCES categorias(id)"))
            db.session.commit()
            print("Alter table successful.")
        except Exception as e:
            print("Already altered or error:", e)

if __name__ == '__main__':
    alter_table()
