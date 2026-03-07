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
        # 1. Create carteiras table
        print("Creating table 'carteiras'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS carteiras (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(50) NOT NULL UNIQUE
            )
        """)

        # 2. Insert initial values
        print("Inserting initial carteiras...")
        carteiras_iniciais = ['Consolidada', 'Leo', 'Leozinho']
        for nome in carteiras_iniciais:
            cursor.execute("INSERT IGNORE INTO carteiras (nome) VALUES (%s)", (nome,))
        
        conn.commit()

        # Get carteira mapping
        cursor.execute("SELECT id, nome FROM carteiras")
        carteira_mapping = {nome: id for id, nome in cursor.fetchall()}
        print(f"Carteira mapping: {carteira_mapping}")

        # 3. Add carteira_id columns to existing tables
        tables = ['ativos', 'vendas', 'dividendos', 'transacoes', 'config_financeiras_fixas']
        
        for table in tables:
            print(f"Adding 'carteira_id' to '{table}'...")
            try:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN carteira_id INT")
                cursor.execute(f"ALTER TABLE {table} ADD CONSTRAINT fk_{table}_carteira FOREIGN KEY (carteira_id) REFERENCES carteiras(id)")
            except mysql.connector.Error as err:
                if err.errno == 1060: # Column already exists
                    print(f"Column 'carteira_id' already exists in '{table}'.")
                else:
                    raise err

        # 4. Migrate data
        for table in tables:
            print(f"Migrating data for '{table}'...")
            for nome, cid in carteira_mapping.items():
                cursor.execute(f"UPDATE {table} SET carteira_id = %s WHERE carteira = %s OR (carteira IS NULL AND %s = 'Consolidada')", (cid, nome, nome))
            
            # For cases where carteiras might be different or null
            cursor.execute(f"UPDATE {table} SET carteira_id = %s WHERE carteira_id IS NULL", (carteira_mapping['Consolidada'],))

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
