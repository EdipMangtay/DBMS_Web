import os
import sys
from dotenv import load_dotenv

load_dotenv()

def create_database():
    db_type = os.getenv('DB_TYPE', 'sqlite')
    
    if db_type == 'sqlite':
        sqlite_file = 'studentsystem.db'
        if os.path.exists(sqlite_file):
            print(f"✓ SQLite veritabanı zaten mevcut: {sqlite_file}")
            return True
        else:
            print(f"✓ SQLite veritabanı oluşturulacak: {sqlite_file}")
            return True
    else:
        try:
            import pymysql
            
            db_host = os.getenv('DB_HOST', '127.0.0.1')
            db_port = int(os.getenv('DB_PORT', 3306))
            db_user = os.getenv('DB_USER', 'root')
            db_password = os.getenv('DB_PASSWORD', '')
            db_name = os.getenv('DB_NAME', 'studentsystem')
            
            print(f"MySQL'e bağlanılıyor... ({db_user}@{db_host}:{db_port})")
            
            connection = pymysql.connect(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_password,
                charset='utf8mb4'
            )
            
            try:
                with connection.cursor() as cursor:
                    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                    print(f"✓ Veritabanı '{db_name}' oluşturuldu veya zaten mevcut.")
                
                connection.commit()
                return True
                
            finally:
                connection.close()
                
        except ImportError:
            print("HATA: pymysql yüklü değil!")
            return False
        except pymysql.Error as e:
            print(f"HATA: MySQL bağlantı hatası: {e}")
            return False
        except Exception as e:
            print(f"HATA: {e}")
            return False

if __name__ == '__main__':
    print("=" * 50)
    print("Veritabanı Oluşturma Scripti")
    print("=" * 50)
    print()
    
    if create_database():
        print()
        print("✓ Veritabanı hazır!")
        sys.exit(0)
    else:
        print()
        print("✗ Veritabanı oluşturulamadı.")
        sys.exit(1)

