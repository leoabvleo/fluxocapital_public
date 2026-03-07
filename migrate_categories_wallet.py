import mysql.connector
import os

def migrate():
    db_user = os.getenv('DB_USER', 'user_fluxocapital')
    db_pass = os.getenv('DB_PASS', '1qhnTXZDCz8P4cB7n')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_name = os.getenv('DB_NAME', 'db_fluxocapital')

    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_name
        )
        cursor = conn.cursor()

        # Tabelas para adicionar carteira_id
        tabelas = ['categoria_ativos', 'categoria_proventos', 'categorias']

        for tabela in tabelas:
            # Verifica se a coluna já existe
            cursor.execute(f"SHOW COLUMNS FROM {tabela} LIKE 'carteira_id'")
            result = cursor.fetchone()
            
            if not result:
                print(f"Adicionando coluna 'carteira_id' na tabela '{tabela}'...")
                # Adiciona a coluna permitindo NULL (Global)
                cursor.execute(f"ALTER TABLE {tabela} ADD COLUMN carteira_id INT NULL")
                # Adiciona o Foreign Key
                cursor.execute(f"ALTER TABLE {tabela} ADD CONSTRAINT fk_{tabela}_carteira FOREIGN KEY (carteira_id) REFERENCES carteiras(id) ON DELETE CASCADE")
                print(f"Coluna e constraint adicionadas em '{tabela}'.")
            else:
                print(f"A coluna 'carteira_id' já existe na tabela '{tabela}'.")

        conn.commit()
        print("Migração concluída com sucesso!")

    except mysql.connector.Error as err:
        print(f"Erro ao conectar ou executar comandos SQL: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    migrate()
