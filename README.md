# 🍽️ Restoran Görü Sistemi (Bilgisayarla Görü Final Projesi)

Bu proje, bir restoran ortamında garsonları QR kod ile tanıyan, yemekleri kamera aracılığıyla tanımlayıp ücretlendiren, garson performansını analiz eden ve günlük raporları oluşturan bir bilgisayarla görü sistemidir.

## 📌 Özellikler

- 📷 QR Kod ile Garson Tanıma
- 🍲 Kamera ile Yemek Tanıma (Derin Öğrenme modeli ile)
- 💳 QR Kod ile Hesap Sıfırlama Sistemi
- 📊 Garson Performans Raporlama
- 📅 Günlük ve tarihsel işlem kayıtları
- 🖥️ Basit Yönetim Paneli (Tkinter tabanlı GUI)

---

## 🔧 Kurulum

### 1. Gerekli Kütüphaneler

```bash
pip install opencv-python
pip install pyzbar
pip install tensorflow
pip install numpy==1.24.3
2. Proje Dosyaları
Aşağıdaki dosyaları aynı klasöre koyduğunuzdan emin olun:

qr_masa_kayit.py – Garson QR kodu tanıma

yemek_tanima.py – Kamera ile yemek tahmini

qr_hesap_sifirla.py – Masa sıfırlama QR sistemi

rapor_olustur.py – Garson performans ve masa bazlı rapor

yemek_modeli.h5 – Eğitilmiş yemek tanıma modeli (MobileNet vb.)

loglar.json – Sistem kayıtlarının tutulduğu dosya

yönetim_paneli.py – Yönetim arayüzü (isteğe bağlı GUI)

▶️ Kullanım
🔹 1. Garson QR Kod ile Tanıtımı
bash
Kopyala
Düzenle
python qr_masa_kayit.py
Garsonlar QR kodlarını kameraya göstererek siparişi alan kişi olarak tanıtılır.

🔹 2. Yemek Tanıma Sistemi
bash
Kopyala
Düzenle
python yemek_tanima.py
Kameradaki odak alanına gelen yemek modeli tanınır ve loglar.json içine yazılır.

🔹 3. Hesap Sıfırlama
bash
Kopyala
Düzenle
python qr_hesap_sifirla.py
Garson, masa bittiğinde ilgili QR kodu göstererek hesap sıfırlanmasını sağlar.

🔹 4. Rapor Oluşturma
bash
Kopyala
Düzenle
python rapor_olustur.py
Garson bazlı yemek sayısı, ciro, geç kalma analizi ve masa bazlı hesaplar konsola ve rapor.json dosyasına yazılır.

🔹 5. Yönetim Paneli (Opsiyonel)
bash
Kopyala
Düzenle
python yönetim_paneli.py
Tkinter tabanlı basit panel ile geçmişe dönük işlemler ve raporlar görüntülenebilir.

📁 Dosya Yapısı
pgsql
Kopyala
Düzenle
📂 bilgisayar-goru
├── yemek_modeli.h5
├── loglar.json
├── rapor.json
├── qr_masa_kayit.py
├── yemek_tanima.py
├── qr_hesap_sifirla.py
├── rapor_olustur.py
├── yönetim_paneli.py
└── README.md
📌 Notlar
Kamera sadece masayı ve koridordan gelen garsonu görecek şekilde konumlandırılmalıdır.

Aynı garsonın aynı masaya tekrar tekrar okutması engellenmiştir.

Geç kalma, müşteri geldikten 60 saniye sonra garson QR okutmazsa loglara yazılmaktadır.

🧠 Kullanılan Teknolojiler
Python

OpenCV

TensorFlow / Keras

Pyzbar

Tkinter

JSON

👤 Geliştirici
📛 Şahi Gül
📘 Bilgisayar Mühendisliği
📅 2025 Final Projesi

yaml
Kopyala
Düzenle

---

### İstersen bu README’yi `.md` veya `.docx` olarak da veririm. Yeterli mi yoksa bir şey daha ekley
