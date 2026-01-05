import os
import sys
import subprocess
from dotenv import load_dotenv

load_dotenv()

def import_sql_file():
    sql_file = 'studentsystem_full.sql'
    
    if not os.path.exists(sql_file):
        print(f"✗ {sql_file} dosyası bulunamadı!")
        return False
    
    db_host = os.getenv('DB_HOST', '127.0.0.1')
    db_port = os.getenv('DB_PORT', '3306')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_name = os.getenv('DB_NAME', 'studentsystem')
    
    print(f"SQL dosyası import ediliyor: {sql_file}")
    print(f"Veritabanı: {db_name}")
    
    try:
        if db_password:
            cmd = [
                'mysql',
                f'-h{db_host}',
                f'-P{db_port}',
                f'-u{db_user}',
                f'-p{db_password}',
                db_name
            ]
        else:
            cmd = [
                'mysql',
                f'-h{db_host}',
                f'-P{db_port}',
                f'-u{db_user}',
                db_name
            ]
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(input=sql_content)
        
        if process.returncode == 0:
            print("✓ SQL dosyası başarıyla import edildi!")
            return True
        else:
            print(f"✗ SQL import hatası: {stderr}")
            print("\nManuel import için:")
            if db_password:
                print(f"  mysql -u {db_user} -p{db_password} {db_name} < {sql_file}")
            else:
                print(f"  mysql -u {db_user} {db_name} < {sql_file}")
            return False
            
    except FileNotFoundError:
        print("✗ MySQL komut satırı aracı bulunamadı!")
        print("MySQL'in yüklü olduğundan ve PATH'de olduğundan emin olun.")
        print("\nManuel import için:")
        print(f"  mysql -u {db_user} -p {db_name} < {sql_file}")
        return False
    except Exception as e:
        print(f"✗ Hata: {e}")
        print("\nManuel import için:")
        print(f"  mysql -u {db_user} -p {db_name} < {sql_file}")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("SQL Import Scripti")
    print("=" * 50)
    print()
    
    if import_sql_file():
        print()
        print("✓ Veritabanı hazır!")
        sys.exit(0)
    else:
        print()
        print("✗ SQL import edilemedi. Lütfen manuel olarak import edin.")
        sys.exit(1)

