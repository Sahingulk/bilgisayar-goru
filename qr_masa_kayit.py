import cv2
from pyzbar.pyzbar import decode
import datetime
import json
import os

MASA_ID = "Masa_1"
LOG_DOSYASI = "loglar.json"

# Logları yükle
if os.path.exists(LOG_DOSYASI):
    with open(LOG_DOSYASI, "r", encoding="utf-8") as f:
        loglar = json.load(f)
else:
    loglar = []

# QR tekrarını engellemek için son kayıt takibi
son_kayitlar = {}

# Kamera başlat
cap = cv2.VideoCapture(0)
print("Garson QR kodunu gösterin...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    qr_codes = decode(frame)

    for code in qr_codes:
        garson_id = code.data.decode('utf-8')
        zaman = datetime.datetime.now()
        zaman_str = zaman.strftime("%Y-%m-%d %H:%M:%S")
        anahtar = f"{MASA_ID}-{garson_id}"

        # Aynı garson aynı masayı 10 saniyede birden fazla okutamasın
        if anahtar in son_kayitlar:
            fark = (zaman - son_kayitlar[anahtar]).total_seconds()
            if fark < 10:
                continue

        # Kaydı yap
        kayit = {
            "masa": MASA_ID,
            "garson": garson_id,
            "zaman": zaman_str
        }
        loglar.append(kayit)
        son_kayitlar[anahtar] = zaman

        print(f"{zaman_str} - {MASA_ID} → {garson_id}")
        with open(LOG_DOSYASI, "w", encoding="utf-8") as f:
            json.dump(loglar, f, indent=4, ensure_ascii=False)

        # Görüntü üzerine yaz
        cv2.putText(frame, f"{MASA_ID} - {garson_id}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

    cv2.imshow("Garson Tanıma (QR)", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
