#!/bin/bash

echo "========================================"
echo "Student System - Çalıştırılıyor"
echo "========================================"
echo ""

if [ ! -d "venv" ]; then
    echo "HATA: Virtual environment bulunamadı!"
    echo "Önce ./setup.sh dosyasını çalıştırın."
    exit 1
fi

source venv/bin/activate
python app.py

