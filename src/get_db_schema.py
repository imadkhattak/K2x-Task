import mysql.connector
from src.db_config import DB_CONFIG

def save_schema_to_file():
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        )
        cursor = conn.cursor()

        with open('src/database/schema.txt', 'w') as f:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            f.write("=== DATABASE SCHEMA ===\n")
            f.write(f"Database: {DB_CONFIG['database']}\n\n")

            for table in tables:
                table_name = table[0]
                f.write(f"TABLE: {table_name}\n")
                f.write("-" * 50 + "\n")

                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()

                for col in columns:
                    f.write(f"{col[0]:<20} {col[1]:<15} {col[2]:<5} {col[3]:<10}\n")
                
                f.write("\n")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

