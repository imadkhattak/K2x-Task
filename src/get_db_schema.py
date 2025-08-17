import os
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

        # ✅ Ensure schema file is saved inside src/database/
        schema_path = os.path.join(os.path.dirname(__file__), "database_schema.txt")

        with open(schema_path, "w", encoding="utf-8") as f:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            for table in tables:
                table_name = table[0]
                f.write(f"Table: {table_name}\n")

                cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                columns = cursor.fetchall()

                for column in columns:
                    f.write(f"  {column[0]} - {column[1]}\n")
                f.write("\n")

        cursor.close()
        conn.close()
        print(f"✅ Schema saved to {schema_path}")

    except Exception as e:
        print(f"❌ Error saving schema: {e}")
