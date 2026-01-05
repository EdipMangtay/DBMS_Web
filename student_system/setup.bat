@echo off
chcp 65001 >nul
echo ========================================
echo Student System - Otomatik Kurulum
echo ========================================
echo.

echo [0/8] .env dosyasi kontrol ediliyor...
if not exist .env (
    echo .env dosyasi olusturuluyor...
    (
        echo DB_TYPE=sqlite
        echo DATABASE_URL=sqlite:///studentsystem.db
        echo DB_HOST=127.0.0.1
        echo DB_PORT=3306
        echo DB_USER=root
        echo DB_PASSWORD=
        echo DB_NAME=studentsystem
        echo SECRET_KEY=dev-secret-key-change-in-production-12345
    ) > .env
    echo .env dosyasi olusturuldu! (SQLite modu)
) else (
    echo .env dosyasi zaten mevcut.
)
echo.

echo [1/8] Virtual Environment olusturuluyor...
if exist venv (
    echo Virtual environment zaten mevcut, atlaniyor...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo HATA: Python bulunamadi! Python 3.8+ yuklu oldugundan emin olun.
        pause
        exit /b 1
    )
)

echo [2/8] Virtual Environment aktif ediliyor...
call venv\Scripts\activate.bat

echo [3/8] Paketler yukleniyor...
pip install --upgrade pip --quiet
pip install -r requirements.txt
if errorlevel 1 (
    echo HATA: Paketler yuklenemedi!
    pause
    exit /b 1
)

echo [4/8] Veritabani tipi kontrol ediliyor...
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('DB_TYPE:', os.getenv('DB_TYPE', 'sqlite'))"
echo.

echo [5/8] SQLite veritabani olusturuluyor...
if exist studentsystem_full.sql (
    echo SQL dosyasi bulundu, SQLite'a import ediliyor...
    python sql_to_sqlite.py
    if errorlevel 1 (
        echo UYARI: SQLite import hatasi! MySQL moduna geciliyor...
        echo DB_TYPE=mysql > .env.tmp
        type .env | findstr /V "DB_TYPE" >> .env.tmp
        move /Y .env.tmp .env >nul
        echo.
        echo [5.5/8] MySQL veritabani olusturuluyor...
        python setup_database.py
        echo [5.6/8] MySQL'e SQL import ediliyor...
        python import_sql.py
    ) else (
        echo SQLite veritabani hazir!
    )
) else (
    echo UYARI: studentsystem_full.sql bulunamadi!
    echo SQLite veritabani bos olarak olusturulacak.
    python -c "import sqlite3; conn = sqlite3.connect('studentsystem.db'); conn.close(); print('SQLite veritabani olusturuldu.')"
)

echo [6/8] MySQL modu kontrol ediliyor...
python -c "from dotenv import load_dotenv; import os; load_dotenv(); db_type = os.getenv('DB_TYPE', 'sqlite'); print('Aktif mod:', db_type)"
if "%DB_TYPE%"=="mysql" (
    echo MySQL modu aktif, veritabani kontrol ediliyor...
    python setup_database.py
    if exist studentsystem_full.sql (
        python import_sql.py
    )
)

echo [7/8] Kurulum tamamlandi!
echo.
echo [8/8] Veritabani hazir!
echo.
echo ========================================
echo Uygulamayi calistirmak icin:
echo   python app.py
echo.
echo Tarayicida acin: http://127.0.0.1:5000
echo.
echo Giris Bilgileri:
echo   Student: edip / edip123
echo   Admin: edip / edip123
echo   Instructor: edip / edip123
echo ========================================
echo.
pause

