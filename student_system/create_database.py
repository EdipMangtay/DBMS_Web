"""
Script to create the StudentSystem database if it doesn't exist.
"""
import pymysql
from config import Config

def create_database():
    try:
        # Connect to MySQL server without specifying database
        connection = pymysql.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{Config.DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"Database '{Config.DB_NAME}' created or already exists!")
        
        cursor.close()
        connection.close()
        
        print("Database setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error creating database: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    create_database()




