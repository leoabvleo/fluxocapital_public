import mysql.connector
import os

# Configuração de Banco de Dados MariaDB/MySQL
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
        # 1. Create perfil_usuario table
        print("Creating table 'perfil_usuario'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS perfil_usuario (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(50) NOT NULL UNIQUE
            )
        """)

        # 2. Insert initial profiles
        print("Inserting initial profiles...")
        perfis = ['Admin', 'Usuário', 'Familiar']
        for p in perfis:
            cursor.execute("INSERT IGNORE INTO perfil_usuario (nome) VALUES (%s)", (p,))
        
        conn.commit()

        # Get profile mapping
        cursor.execute("SELECT id, nome FROM perfil_usuario")
        profile_mapping = {nome.lower(): id for id, nome in cursor.fetchall()}
        print(f"Profile mapping: {profile_mapping}")

        # 3. Add perfil_id column to usuarios table
        print("Adding 'perfil_id' column to 'usuarios' table...")
        try:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN perfil_id INT")
            cursor.execute("ALTER TABLE usuarios ADD CONSTRAINT fk_usuario_perfil FOREIGN KEY (perfil_id) REFERENCES perfil_usuario(id)")
        except mysql.connector.Error as err:
            if err.errno == 1060: # Column already exists
                print("Column 'perfil_id' already exists in 'usuarios'.")
            else:
                raise err

        # 4. Migrate data
        print("Migrating profile data...")
        # Get existing users and their perfil string
        cursor.execute("SELECT id, perfil FROM usuarios")
        users = cursor.fetchall()
        
        for u_id, p_str in users:
            if p_str:
                p_key = p_str.lower()
                # Map 'admin' to 'admin', 'usuario' to 'usuário', etc.
                if p_key == 'admin':
                    p_id = profile_mapping['admin']
                elif p_key == 'usuario':
                    p_id = profile_mapping['usuário']
                elif p_key == 'familiar':
                    p_id = profile_mapping['familiar']
                else:
                    p_id = profile_mapping['usuário'] # Default
                
                cursor.execute("UPDATE usuarios SET perfil_id = %s WHERE id = %s", (p_id, u_id))

        conn.commit()

        # 5. Drop old perfil column
        print("Dropping old 'perfil' column...")
        try:
            cursor.execute("ALTER TABLE usuarios DROP COLUMN perfil")
        except mysql.connector.Error as err:
            print(f"Warning dropping column: {err}")

        conn.commit()
        print("Migration completed successfully!")

    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    migrate()
