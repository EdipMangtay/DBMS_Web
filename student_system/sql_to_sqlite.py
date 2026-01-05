import sqlite3
import os
import sys
import re
from app import create_app
from database import db

def import_sql_to_sqlite():
    sql_file = 'studentsystem_full.sql'
    sqlite_file = 'studentsystem.db'
    
    if not os.path.exists(sql_file):
        print(f"HATA: {sql_file} dosyasi bulunamadi!")
        return False
    
    print("=" * 60)
    print("SQL Dump'tan SQLite'a Import")
    print("=" * 60)
    print()
    
    try:
        app = create_app()
        with app.app_context():
            if os.path.exists(sqlite_file):
                print(f"Mevcut SQLite dosyasi siliniyor: {sqlite_file}")
                os.remove(sqlite_file)
            
            print("SQLAlchemy modellerinden tablolar olusturuluyor...")
            db.create_all()
            print("OK Tablolar olusturuldu")
            print()
            
            print("SQL dosyasindan veriler import ediliyor...")
            with open(sql_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
            content = re.sub(r'--.*', '', content)
            content = re.sub(r'LOCK TABLES.*?UNLOCK TABLES;', '', content, flags=re.DOTALL)
            content = re.sub(r'ALTER TABLE.*?ENABLE KEYS;', '', content, flags=re.DOTALL)
            content = re.sub(r'DISABLE KEYS;', '', content, flags=re.DOTALL)
            
            sqlite_conn = sqlite3.connect(sqlite_file)
            sqlite_cursor = sqlite_conn.cursor()
            
            insert_pattern = re.compile(r'INSERT\s+INTO\s+`?(\w+)`?\s+VALUES\s+(.+?)(?=INSERT\s+INTO|$)', re.IGNORECASE | re.DOTALL)
            matches = insert_pattern.finditer(content)
            
            total_inserts = 0
            
            for match in matches:
                table_name = match.group(1)
                values_part = match.group(2).strip().rstrip(';')
                
                values_list = []
                current_value = ""
                paren_depth = 0
                in_string = False
                string_char = None
                
                for char in values_part:
                    if char in ("'", '"') and (not current_value or current_value[-1] != '\\'):
                        if not in_string:
                            in_string = True
                            string_char = char
                        elif char == string_char:
                            in_string = False
                            string_char = None
                        current_value += char
                    elif not in_string:
                        if char == '(':
                            paren_depth += 1
                            current_value += char
                        elif char == ')':
                            paren_depth -= 1
                            current_value += char
                            if paren_depth == 0:
                                values_list.append(current_value.strip())
                                current_value = ""
                        elif char == ',' and paren_depth == 0:
                            if current_value.strip():
                                values_list.append(current_value.strip())
                                current_value = ""
                        else:
                            current_value += char
                    else:
                        current_value += char
                
                if current_value.strip():
                    values_list.append(current_value.strip())
                
                for value_tuple in values_list:
                    try:
                        sqlite_cursor.execute(f"INSERT INTO `{table_name}` VALUES {value_tuple}")
                        total_inserts += 1
                    except sqlite3.IntegrityError:
                        pass
                    except Exception as e:
                        if 'no such table' not in str(e).lower():
                            print(f"  UYARI: {table_name} - {str(e)[:60]}")
            
            sqlite_conn.commit()
            sqlite_cursor.close()
            sqlite_conn.close()
            
            print()
            print("=" * 60)
            print(f"OK Import tamamlandi!")
            print(f"OK {total_inserts} kayit eklendi")
            print(f"OK SQLite dosyasi: {os.path.abspath(sqlite_file)}")
            if os.path.exists(sqlite_file):
                print(f"OK Dosya boyutu: {os.path.getsize(sqlite_file) / 1024:.2f} KB")
            print("=" * 60)
            return True
        
    except Exception as e:
        print(f"\nHATA: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    import_sql_to_sqlite()
