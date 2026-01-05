@echo off
chcp 65001 >nul
echo ========================================
echo Student System - Calistiriliyor
echo ========================================
echo.

if not exist venv (
    echo HATA: Virtual environment bulunamadi!
    echo Once setup.bat dosyasini calistirin.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
python app.py

