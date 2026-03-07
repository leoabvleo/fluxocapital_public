from app import app, db, Usuario
from werkzeug.security import generate_password_hash
import sys

def reset_password(username, new_password):
    with app.app_context():
        user = Usuario.query.filter_by(username=username).first()
        if not user:
            print(f"Erro: Usuário '{username}' não encontrado.")
            return

        # Força o uso de pbkdf2:sha256 que é suportado em qualquer lugar
        # O erro 'hashlib has no attribute scrypt' acontece porque o Python local
        # não foi compilado com OpenSSL 1.1+ ou similar.
        new_hash = generate_password_hash(new_password, method='pbkdf2:sha256')
        
        user.password = new_hash
        db.session.commit()
        print(f"Sucesso! Senha do usuário '{username}' alterada para '{new_password}'.")
        print("Tente fazer login novamente.")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        reset_password(sys.argv[1], sys.argv[2])
    else:
        # Padrão: usuário 'leonardo' (do dump) e senha '123456'
        # Se seu usuário for outro, edite aqui ou passe como argumento
        print("Uso: python3 reset_password.py <usuario> <nova_senha>")
        print("Tentando resetar usuário padrão 'leonardo' para senha '123456'...")
        reset_password('leonardo', '123456')
