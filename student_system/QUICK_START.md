# 🚀 Hızlı Başlangıç - Tek Komutla Çalıştır!

## Windows Kullanıcıları:

### İlk Kurulum:
1. **setup.bat** dosyasına çift tıklayın
2. Kurulum tamamlanana kadar bekleyin
3. **run.bat** dosyasına çift tıklayın
4. Tarayıcıda açın: http://127.0.0.1:5000

### Sonraki Kullanımlar:
- Sadece **run.bat** dosyasına çift tıklayın!

## Linux/Mac Kullanıcıları:

### İlk Kurulum:
```bash
chmod +x setup.sh run.sh
./setup.sh
```

### Çalıştırma:
```bash
./run.sh
```

Veya:
```bash
source venv/bin/activate
python app.py
```

## 🔑 Giriş Bilgileri:

- **Student**: `edip` / `edip123`
- **Admin**: `edip` / `edip123`
- **Instructor**: `edip` / `edip123`

## ⚠️ Önemli Notlar:

1. **MySQL'in çalıştığından emin olun!**
2. Eğer MySQL şifreniz varsa, `.env` dosyasını düzenleyin
3. SQL dump dosyası (`studentsystem_full.sql`) projede olmalı

## 🐛 Sorun Giderme:

### "MySQL bulunamadı" hatası:
- MySQL'in PATH'de olduğundan emin olun
- Veya SQL dosyasını manuel import edin:
  ```bash
  mysql -u root -p studentsystem < studentsystem_full.sql
  ```

### "Port 5000 kullanımda" hatası:
- `app.py` dosyasında port numarasını değiştirin
- Veya çalışan uygulamayı kapatın

### "Module not found" hatası:
- Virtual environment'ın aktif olduğundan emin olun
- `pip install -r requirements.txt` çalıştırın

---

**Hepsi bu kadar!** 🎉

