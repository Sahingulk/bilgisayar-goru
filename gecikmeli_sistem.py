import cv2
import datetime
import json
import os
from pyzbar.pyzbar import decode
import time

MASA_ID = "Masa_1"
LOG_DOSYASI = "loglar.json"

if os.path.exists(LOG_DOSYASI):
    with open(LOG_DOSYASI, "r", encoding="utf-8") as f:
        loglar = json.load(f)
else:
    loglar = []

cap = cv2.VideoCapture(0)

müşteri_zamanı = None
garson_geldi = False
son_garson = None

print("⚙️ Sistem hazır. 'M' → müşteri geldi. 1 dakika içinde QR okunmalı!")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ==== QR OKUMA ====
    qr_codes = decode(frame)
    for code in qr_codes:
        son_garson = code.data.decode('utf-8')
        garson_geldi = True
        cv2.putText(frame, f"Garson: {son_garson}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

    # ==== Tuşlar ====
    key = cv2.waitKey(1) & 0xFF

    # Müşteri gelişi
    if key == ord('m'):
        müşteri_zamanı = time.time()
        garson_geldi = False
        son_garson = None
        print(f"🟢 Müşteri geldi → {MASA_ID} (başlangıç zamanı alındı)")

    # Çıkış
    elif key == ord('q'):
        break

    # ==== 1 dakikalık süre kontrolü ====
    if müşteri_zamanı and not garson_geldi:
        geçen_süre = time.time() - müşteri_zamanı
        if geçen_süre > 60:
            print(f"⚠️ {MASA_ID} için GARSON GEÇ KALDI ({int(geçen_süre)} sn)")

            zaman = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            kayit = {
                "masa": MASA_ID,
                "garson": son_garson if son_garson else "Belirsiz",
                "zaman": zaman,
                "gec_kalma": True
            }
            if kayit not in loglar:
                loglar.append(kayit)
                with open(LOG_DOSYASI, "w", encoding="utf-8") as f:
                    json.dump(loglar, f, indent=4, ensure_ascii=False)

            müşteri_zamanı = None  # kontrol tamamlandı, sıfırla

    cv2.imshow("Garson Gecikme Takibi", frame)

cap.release()
cv2.destroyAllWindows()
