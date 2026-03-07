import mysql.connector
import os

db_user = os.environ.get('DB_USER', 'user_fluxocapital')
db_pass = os.environ.get('DB_PASS', '1qhnTXZDCz8P4cB7n')
db_host = os.environ.get('DB_HOST', 'localhost')
db_name = os.environ.get('DB_NAME', 'db_fluxocapital')

def migrate():
    conn = mysql.connector.connect(
        user=db_user,
        password=db_pass,
        host=db_host,
        database=db_name
    )
    cursor = conn.cursor()

    try:
        # 1. Ensure SuperAdmin profile exists
        print("Garantindo perfil 'SuperAdmin' na tabela 'perfil_usuario'...")
        cursor.execute("INSERT IGNORE INTO perfil_usuario (nome) VALUES ('SuperAdmin')")
        conn.commit()
        print("Perfil 'SuperAdmin' inserido (ou já existia).")

        # 2. Show current profiles
        cursor.execute("SELECT id, nome FROM perfil_usuario ORDER BY id")
        perfis = cursor.fetchall()
        print("\nPerfis atuais no banco:")
        for pid, pnome in perfis:
            print(f"  id={pid}  nome={pnome}")

        # 3. Optional: assign first user as SuperAdmin (manual step)
        print("\nMigração concluída! Para atribuir SuperAdmin a um usuário, acesse")
        print("a página de Gestão de Usuários e altere o perfil no painel.")

    except Exception as e:
        print(f"Erro durante a migração: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    migrate()
