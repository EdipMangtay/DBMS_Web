"""
Check existing tables in the database.
"""
import pymysql
from config import Config

def check_tables():
    try:
        connection = pymysql.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        
        cursor = connection.cursor()
        
        # Get all tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"\nMevcut tablolar ({Config.DB_NAME} veritabanında):")
        print("=" * 50)
        for table in tables:
            print(f"  - {table[0]}")
        
        cursor.close()
        connection.close()
        
        return [table[0] for table in tables]
        
    except Exception as e:
        print(f"Hata: {str(e)}")
        return []

if __name__ == '__main__':
    check_tables()




