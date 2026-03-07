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
        # 1. Add perfil column to usuarios table
        print("Adding 'perfil' column to 'usuarios' table...")
        try:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN perfil VARCHAR(20) DEFAULT 'admin'")
            print("Column 'perfil' added successfully.")
        except mysql.connector.Error as err:
            if err.errno == 1060: # Column already exists
                print("Column 'perfil' already exists in 'usuarios'.")
            else:
                raise err

        # 2. Update existing users to 'admin' (though DEFAULT 'admin' should handle it)
        print("Ensuring all users have 'admin' perfil...")
        cursor.execute("UPDATE usuarios SET perfil = 'admin' WHERE perfil IS NULL")
        
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
