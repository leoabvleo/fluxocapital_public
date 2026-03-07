import mysql.connector
import os

db_user = os.environ.get('DB_USER', 'user_fluxocapital')
db_pass = os.environ.get('DB_PASS', '1qhnTXZDCz8P4cB7n')
db_host = os.environ.get('DB_HOST', 'localhost')
db_name = os.environ.get('DB_NAME', 'db_fluxocapital')

def create_table():
    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_name
        )
        cursor = conn.cursor()
        
        query = """
        CREATE TABLE IF NOT EXISTS usuario_carteira (
            usuario_id INT NOT NULL,
            carteira_id INT NOT NULL,
            PRIMARY KEY (usuario_id, carteira_id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY (carteira_id) REFERENCES carteiras(id) ON DELETE CASCADE
        )
        """
        cursor.execute(query)
        conn.commit()
        print("Table `usuario_carteira` created successfully.")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    create_table()
