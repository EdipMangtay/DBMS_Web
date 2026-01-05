#!/bin/bash

echo "========================================"
echo "Student System - Otomatik Kurulum"
echo "========================================"
echo ""

echo "[0/8] .env dosyası kontrol ediliyor..."
if [ ! -f ".env" ]; then
    echo ".env dosyası oluşturuluyor..."
    cat > .env << EOF
DB_TYPE=sqlite
DATABASE_URL=sqlite:///studentsystem.db
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=studentsystem
SECRET_KEY=dev-secret-key-change-in-production-12345
EOF
    echo ".env dosyası oluşturuldu! (SQLite modu)"
else
    echo ".env dosyası zaten mevcut."
fi
echo ""

echo "[1/8] Virtual Environment oluşturuluyor..."
if [ -d "venv" ]; then
    echo "Virtual environment zaten mevcut, atlanıyor..."
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "HATA: Python bulunamadı! Python 3.8+ yüklü olduğundan emin olun."
        exit 1
    fi
fi

echo "[2/6] Virtual Environment aktif ediliyor..."
source venv/bin/activate

echo "[3/6] Paketler yükleniyor..."
pip install --upgrade pip --quiet
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "HATA: Paketler yüklenemedi!"
    exit 1
fi

echo "[4/8] Veritabanı tipi kontrol ediliyor..."
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print('DB_TYPE:', os.getenv('DB_TYPE', 'sqlite'))"
echo ""

echo "[5/8] SQLite veritabanı oluşturuluyor..."
if [ -f "studentsystem_full.sql" ]; then
    echo "SQL dosyası bulundu, SQLite'a import ediliyor..."
    python3 sql_to_sqlite.py
    if [ $? -ne 0 ]; then
        echo "UYARI: SQLite import hatası! MySQL moduna geçiliyor..."
        echo "DB_TYPE=mysql" > .env.tmp
        grep -v "DB_TYPE" .env >> .env.tmp
        mv .env.tmp .env
        echo ""
        echo "[5.5/8] MySQL veritabanı oluşturuluyor..."
        python3 setup_database.py
        echo "[5.6/8] MySQL'e SQL import ediliyor..."
        python3 import_sql.py
    else
        echo "SQLite veritabanı hazır!"
    fi
else
    echo "UYARI: studentsystem_full.sql bulunamadı!"
    echo "SQLite veritabanı boş olarak oluşturulacak."
    python3 -c "import sqlite3; conn = sqlite3.connect('studentsystem.db'); conn.close(); print('SQLite veritabanı oluşturuldu.')"
fi

echo "[6/8] MySQL modu kontrol ediliyor..."
DB_TYPE=$(python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('DB_TYPE', 'sqlite'))")
if [ "$DB_TYPE" = "mysql" ]; then
    echo "MySQL modu aktif, veritabanı kontrol ediliyor..."
    python3 setup_database.py
    if [ -f "studentsystem_full.sql" ]; then
        python3 import_sql.py
    fi
fi

echo "[7/8] Kurulum tamamlandı!"
echo ""
echo "[8/8] Veritabanı hazır!"
echo ""
echo "========================================"
echo "Uygulamayı çalıştırmak için:"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "Tarayıcıda açın: http://127.0.0.1:5000"
echo ""
echo "Giriş Bilgileri:"
echo "  Student: edip / edip123"
echo "  Admin: edip / edip123"
echo "  Instructor: edip / edip123"
echo "========================================"
echo ""

