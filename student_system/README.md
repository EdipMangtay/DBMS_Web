# Student System - Flask Web Application

Öğrenci ve Not Yönetim Sistemi - Role-based access control ile (Admin, Instructor, Student)

**🚀 GitHub'dan indirip direkt çalıştırın!** Windows için `setup.bat`, Linux/Mac için `./setup.sh`

## 📋 Özellikler

- ✅ **Otomatik Kurulum**: Tek komutla tüm bağımlılıklar yüklenir
- ✅ **SQLite & MySQL Desteği**: İki veritabanı seçeneği (varsayılan: SQLite)
- ✅ **Otomatik Veritabanı Oluşturma**: SQL dump'tan otomatik import
- ✅ **Hazır Veriler**: Örnek öğrenci, öğretmen, ders ve not verileri
- ✅ **Role-Based Access**: Admin, Instructor, Student rolleri
- ✅ **Responsive Design**: Bootstrap 5 ile modern arayüz

## 🚀 Hızlı Başlangıç

### Windows Kullanıcıları:

1. **Projeyi indirin** (GitHub'dan ZIP olarak veya `git clone`)
2. **setup.bat** dosyasına çift tıklayın
3. Kurulum tamamlanana kadar bekleyin
4. **run.bat** dosyasına çift tıklayın
5. Tarayıcıda açın: **http://127.0.0.1:5000**

### Linux/Mac Kullanıcıları:

```bash
chmod +x setup.sh run.sh
./setup.sh
./run.sh
```

**Hepsi bu kadar!** 🎉

## 🔑 Giriş Bilgileri

Tüm roller için aynı kullanıcı adı ve şifre:
- **Kullanıcı Adı**: `edip`
- **Şifre**: `edip123`
- **Roller**: Student, Admin, Instructor (giriş sayfasından seçin)

## 📦 Kurulum Detayları

### Otomatik Kurulum Ne Yapar?

1. **Virtual Environment Oluşturur**: Python bağımlılıklarını izole eder
2. **Paketleri Yükler**: `requirements.txt`'deki tüm paketleri kurar
3. **Veritabanı Hazırlar**:
   - **SQLite Modu (Varsayılan)**: `studentsystem_full.sql` dosyasını SQLite'a import eder
   - **MySQL Modu**: MySQL sunucusuna bağlanıp veritabanı oluşturur ve import eder
4. **.env Dosyası Oluşturur**: Gerekli ayarları yapar

### Veritabanı Seçimi

**Varsayılan: SQLite** (MySQL gerekmez, dosya tabanlı)

SQLite kullanmak için `.env` dosyasında:
```
DB_TYPE=sqlite
DATABASE_URL=sqlite:///studentsystem.db
```

MySQL kullanmak için `.env` dosyasında:
```
DB_TYPE=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=studentsystem
```

### Manuel Kurulum (İsteğe Bağlı)

Eğer otomatik kurulum çalışmazsa:

#### 1. Python ve Gereksinimler

- Python 3.8 veya üzeri
- MySQL Server (sadece MySQL modu için)

#### 2. Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Paketleri Yükleyin

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Veritabanını Hazırlayın

**SQLite (Önerilen - Kolay):**
```bash
python sql_to_sqlite.py
```

**MySQL:**
```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS studentsystem;"
python import_sql.py
```

#### 5. Uygulamayı Çalıştırın

```bash
python app.py
```

Tarayıcıda açın: **http://127.0.0.1:5000**

## 📁 Proje Yapısı

```
student_system/
├── app.py                    # Flask uygulama
├── config.py                  # Yapılandırma (SQLite/MySQL desteği)
├── requirements.txt           # Python bağımlılıkları
├── .env                       # Ortam değişkenleri (otomatik oluşturulur)
├── setup.bat                  # Windows otomatik kurulum
├── setup.sh                   # Linux/Mac otomatik kurulum
├── run.bat                    # Windows çalıştırma
├── run.sh                     # Linux/Mac çalıştırma
├── setup_database.py         # Veritabanı oluşturma
├── import_sql.py              # MySQL import scripti
├── sql_to_sqlite.py          # SQL dump'tan SQLite'a import
├── mysql_to_sqlite.py        # MySQL'den SQLite'a export
├── studentsystem_full.sql    # Veritabanı dump (projede mevcut)
├── studentsystem.db          # SQLite veritabanı (otomatik oluşturulur)
├── controllers/              # Route handlers
├── models/                   # SQLAlchemy modelleri
├── repositories/             # Veritabanı işlemleri
├── services/                 # İş mantığı
└── templates/                # HTML şablonları
```

## 🎯 Kullanım Senaryoları

### Senaryo 1: GitHub'dan İndirip Çalıştırma

1. GitHub'dan ZIP indirin
2. Klasöre çıkartın
3. `setup.bat` (Windows) veya `./setup.sh` (Linux/Mac) çalıştırın
4. `run.bat` (Windows) veya `./run.sh` (Linux/Mac) çalıştırın
5. Tarayıcıda `http://127.0.0.1:5000` açın

**Sonuç**: SQLite modunda otomatik çalışır, MySQL gerekmez!

### Senaryo 2: MySQL Kullanma

1. `.env` dosyasını düzenleyin:
   ```
   DB_TYPE=mysql
   DB_PASSWORD=your_mysql_password
   ```
2. MySQL sunucusunun çalıştığından emin olun
3. `setup.bat` veya `./setup.sh` çalıştırın
4. Otomatik olarak MySQL'e bağlanır ve veritabanı oluşturur

### Senaryo 3: Mevcut MySQL Veritabanından SQLite'a Geçiş

1. MySQL modunda çalıştırın ve verileri doldurun
2. `python mysql_to_sqlite.py` çalıştırın
3. `.env` dosyasında `DB_TYPE=sqlite` yapın
4. Uygulamayı yeniden başlatın

## 🔧 Sorun Giderme

### "Python bulunamadı" Hatası

- Python 3.8+ yüklü olduğundan emin olun
- PATH'e eklendiğinden emin olun
- Test: `python --version` veya `python3 --version`

### "Paketler yüklenemedi" Hatası

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### "Veritabanı bağlantı hatası" (MySQL)

- MySQL sunucusunun çalıştığından emin olun
- `.env` dosyasındaki şifreyi kontrol edin
- Test: `mysql -u root -p -h 127.0.0.1`

### "SQLite import hatası"

- `studentsystem_full.sql` dosyasının mevcut olduğundan emin olun
- Dosya izinlerini kontrol edin
- Alternatif: MySQL moduna geçin (otomatik)

### Port 5000 Kullanımda

`app.py` dosyasında port numarasını değiştirin:
```python
app.run(debug=True, port=5001)
```

### Virtual Environment Hatası

- Virtual environment'ın aktif olduğundan emin olun
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

## 📊 Veritabanı İçeriği

Projede `studentsystem_full.sql` dosyası ile birlikte gelir:
- ✅ 11 ders (courses)
- ✅ 10+ öğrenci (students)
- ✅ 11+ öğretmen (instructors)
- ✅ 12 kayıt (enrollments)
- ✅ 12 not (grades)
- ✅ Hazır kullanıcılar (edip_student, edip_admin, edip_instructor)

## 🎓 Özellikler

### Admin Dashboard
- Öğrenci yönetimi (CRUD)
- Öğretmen yönetimi (CRUD)
- Ders yönetimi (CRUD)
- Dönem oluşturma
- Bölüm oluşturma
- Öğrenci kayıt işlemleri
- Raporlar (ders performansı)

### Instructor Dashboard
- Atanan bölümleri görüntüleme
- Öğrenci notlarını girme/güncelleme
- Bölüm istatistikleri (ortalama, min, max)
- Ders istatistikleri

### Student Dashboard
- Kayıtlı dersleri görüntüleme
- Not ortalamalarını görüntüleme
- Transkript görüntüleme
- Harf notları

## 🔒 Güvenlik

- Password hashing (Werkzeug)
- CSRF koruması (Flask-WTF)
- Role-based access control
- SQL injection koruması
- Ortam değişkenleri ile hassas veriler

## 📝 Logging

Uygulama logları `logs/student_system.log` dosyasına yazılır (maksimum 10MB, 10 yedek).

## 🚀 Production Deployment

Production için:

1. `.env` dosyasında `FLASK_ENV=production` ayarlayın
2. Güçlü bir `SECRET_KEY` belirleyin
3. Production WSGI sunucusu kullanın (örn: Gunicorn)
4. HTTPS yapılandırın
5. Veritabanı bağlantı havuzu yapılandırın

## 📄 Lisans

Bu proje eğitim amaçlı olarak sağlanmıştır.

## 💡 İpuçları

- **İlk Kurulum**: SQLite modunu kullanın (MySQL gerekmez)
- **Veri Yedekleme**: `studentsystem.db` dosyasını yedekleyin
- **MySQL'e Geçiş**: `.env` dosyasında `DB_TYPE=mysql` yapın
- **SQLite'a Geçiş**: `python mysql_to_sqlite.py` çalıştırın

## 🆘 Yardım

Sorun yaşarsanız:
1. `logs/student_system.log` dosyasını kontrol edin
2. Virtual environment'ın aktif olduğundan emin olun
3. Tüm bağımlılıkların yüklü olduğundan emin olun
4. Veritabanı bağlantı ayarlarını kontrol edin

---

**Hazırlayan**: Student System Development Team  
**Versiyon**: 1.0  
**Son Güncelleme**: 2026
