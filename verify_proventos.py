from app import app
from models import Dividendo

def verify():
    with app.app_context():
        # Check first 5 dividendos
        divs = Dividendo.query.limit(5).all()
        print("Checking first 5 dividendos:")
        for d in divs:
            cat_nome = d.categoria_provento.nome if d.categoria_provento else "None"
            print(f"ID: {d.id}, Ticker: {d.ticker}, Tipo: {d.tipo}, Cat ID: {d.categoria_provento_id}, Cat Nome: {cat_nome}")
        
        # Check if any have null cat id
        null_count = Dividendo.query.filter(Dividendo.categoria_provento_id == None).count()
        print(f"\nDividendos with null categoria_provento_id: {null_count}")

if __name__ == '__main__':
 verify()
