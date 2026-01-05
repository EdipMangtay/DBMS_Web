import pymysql
import sqlite3
import os
import sys
import re
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def export_mysql_to_sqlite():
    mysql_config = {
        'host': os.getenv('DB_HOST', '127.0.0.1'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'studentsystem'),
        'charset': 'utf8mb4'
    }
    
    sqlite_file = 'studentsystem.db'
    
    print("=" * 60)
    print("MySQL'den SQLite'a Export")
    print("=" * 60)
    print()
    
    try:
        print(f"MySQL'e bağlanılıyor: {mysql_config['user']}@{mysql_config['host']}:{mysql_config['port']}")
        mysql_conn = pymysql.connect(**mysql_config)
        mysql_cursor = mysql_conn.cursor(pymysql.cursors.DictCursor)
        
        if os.path.exists(sqlite_file):
            print(f"Mevcut SQLite dosyası siliniyor: {sqlite_file}")
            os.remove(sqlite_file)
        
        print(f"SQLite veritabanı oluşturuluyor: {sqlite_file}")
        sqlite_conn = sqlite3.connect(sqlite_file)
        sqlite_cursor = sqlite_conn.cursor()
        
        mysql_cursor.execute("SHOW TABLES")
        table_rows = mysql_cursor.fetchall()
        tables = []
        for row in table_rows:
            for key, value in row.items():
                if 'Tables_in' in key:
                    tables.append(value)
                    break
        if not tables:
            tables = [list(row.values())[0] for row in table_rows]
        
        print(f"\n{len(tables)} tablo bulundu: {', '.join(tables)}")
        print()
        
        for table in tables:
            print(f"  [{tables.index(table) + 1}/{len(tables)}] {table} export ediliyor...")
            
            mysql_cursor.execute(f"SHOW CREATE TABLE `{table}`")
            create_table_sql = mysql_cursor.fetchone()['Create Table']
            
            create_table_sql = re.sub(r'`(\w+)`\s+int\s+NOT\s+NULL\s+AUTO_INCREMENT', r'`\1` INTEGER PRIMARY KEY AUTOINCREMENT', create_table_sql, flags=re.IGNORECASE)
            create_table_sql = re.sub(r'`(\w+)`\s+int\s+NOT\s+NULL', r'`\1` INTEGER NOT NULL', create_table_sql, flags=re.IGNORECASE)
            create_table_sql = re.sub(r'`(\w+)`\s+int\s+', r'`\1` INTEGER ', create_table_sql, flags=re.IGNORECASE)
            create_table_sql = create_table_sql.replace('AUTO_INCREMENT', '')
            create_table_sql = create_table_sql.replace('ENGINE=InnoDB', '')
            create_table_sql = create_table_sql.replace('DEFAULT CHARSET=utf8mb4', '')
            create_table_sql = re.sub(r'COLLATE\s+utf8mb4_unicode_ci', '', create_table_sql, flags=re.IGNORECASE)
            create_table_sql = create_table_sql.replace('unsigned', '')
            create_table_sql = create_table_sql.replace('CURRENT_TIMESTAMP', "CURRENT_TIMESTAMP")
            create_table_sql = create_table_sql.replace('curdate()', "date('now')")
            create_table_sql = create_table_sql.replace('now()', "datetime('now')")
            create_table_sql = create_table_sql.replace('tinyint(1)', 'INTEGER')
            create_table_sql = re.sub(r'DEFAULT \(curdate\(\)\)', "DEFAULT (date('now'))", create_table_sql)
            create_table_sql = re.sub(r'DEFAULT \(now\(\)\)', "DEFAULT (datetime('now'))", create_table_sql)
            create_table_sql = re.sub(r',\s*PRIMARY KEY\s*\([^)]+\)', '', create_table_sql, flags=re.IGNORECASE)
            create_table_sql = re.sub(r'PRIMARY KEY\s*\([^)]+\),', '', create_table_sql, flags=re.IGNORECASE)
            
            sqlite_cursor.execute(create_table_sql)
            
            mysql_cursor.execute(f"SELECT * FROM `{table}`")
            rows = mysql_cursor.fetchall()
            
            if rows:
                columns = list(rows[0].keys())
                placeholders = ','.join(['?' for _ in columns])
                columns_str = ','.join([f'`{col}`' for col in columns])
                
                for row in rows:
                    values = []
                    for col in columns:
                        val = row[col]
                        if isinstance(val, datetime):
                            val = val.strftime('%Y-%m-%d %H:%M:%S')
                        values.append(val)
                    sqlite_cursor.execute(
                        f"INSERT INTO `{table}` ({columns_str}) VALUES ({placeholders})",
                        values
                    )
                
                print(f"    ✓ {len(rows)} kayıt eklendi")
            else:
                print(f"    ✓ Tablo boş")
        
        sqlite_conn.commit()
        sqlite_cursor.close()
        sqlite_conn.close()
        mysql_cursor.close()
        mysql_conn.close()
        
        print()
        print("=" * 60)
        print(f"✓ Export tamamlandı!")
        print(f"✓ SQLite dosyası: {os.path.abspath(sqlite_file)}")
        print(f"✓ Dosya boyutu: {os.path.getsize(sqlite_file) / 1024:.2f} KB")
        print("=" * 60)
        return True
        
    except ImportError:
        print("HATA: pymysql yüklü değil! 'pip install pymysql' çalıştırın.")
        return False
    except pymysql.Error as e:
        print(f"HATA: MySQL bağlantı hatası: {e}")
        print("MySQL'in çalıştığından ve kullanıcı adı/şifrenin doğru olduğundan emin olun.")
        return False
    except Exception as e:
        print(f"HATA: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    export_mysql_to_sqlite()

