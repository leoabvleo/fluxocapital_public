from app import app, db
from models import Transacao
import sqlalchemy as sa
with app.app_context():
    anos = db.session.query(sa.extract('year', Transacao.data), db.func.count(Transacao.id)).group_by(sa.extract('year', Transacao.data)).all()
    print("Transacoes", anos)
