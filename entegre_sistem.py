# import cv2
# import numpy as np
# import datetime
# import json
# import os
# from pyzbar.pyzbar import decode
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing.image import img_to_array

# # ====== Ayarlar ======
# MASA_ID = "Masa_1"
# MODEL_YOLU = "yemek_modeli.h5"
# LOG_DOSYASI = "loglar.json"
# SINIFLAR = ['baklava', 'caesar_salad', 'chicken_wings', 'hot_and_sour_soup', 'waffles']
# IMG_SIZE = 224

# # ====== Model Yükle ======
# model = load_model(MODEL_YOLU)

# # ====== Log Yükle ======
# if os.path.exists(LOG_DOSYASI):
#     with open(LOG_DOSYASI, "r", encoding="utf-8") as f:
#         loglar = json.load(f)
# else:
#     loglar = []

# # ====== Kamera Başlat ======
# cap = cv2.VideoCapture(0)
# print("Sistem çalışıyor. QR gösterin, yemek gelsin 😎")

# son_garson = None  # Son QR koddan alınan garson ID

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # ==== QR OKUMA ====
#     qr_codes = decode(frame)
#     for code in qr_codes:
#         son_garson = code.data.decode('utf-8')
#         cv2.putText(frame, f"Garson: {son_garson}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

#     # ==== ORTADAN YEMEK TAHMİNİ ====
#     h, w, _ = frame.shape
#     cx, cy = w // 2, h // 2
#     roi = frame[cy - IMG_SIZE//2:cy + IMG_SIZE//2, cx - IMG_SIZE//2:cx + IMG_SIZE//2]

#     if roi.shape[0] == IMG_SIZE and roi.shape[1] == IMG_SIZE:
#         img = cv2.resize(roi, (IMG_SIZE, IMG_SIZE))
#         img = img_to_array(img) / 255.0
#         img = np.expand_dims(img, axis=0)

#         preds = model.predict(img)[0]
#         yemek = SINIFLAR[np.argmax(preds)]
#         confidence = np.max(preds)

#         cv2.putText(frame, f"Yemek: {yemek} ({confidence*100:.1f}%)", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 200, 0), 2)

#         # ==== KAYIT ====
#         if son_garson and confidence > 0.80:
#             zaman = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             kayit = {
#                 "masa": MASA_ID,
#                 "garson": son_garson,
#                 "yemek": yemek,
#                 "zaman": zaman
#             }

#             if kayit not in loglar:
#                 loglar.append(kayit)
#                 print(f"{zaman} - {MASA_ID} → {son_garson} → {yemek}")
#                 with open(LOG_DOSYASI, "w", encoding="utf-8") as f:
#                     json.dump(loglar, f, indent=4, ensure_ascii=False)

#     # ==== Odak Karesi ====
#     cv2.rectangle(frame, (cx - IMG_SIZE//2, cy - IMG_SIZE//2), (cx + IMG_SIZE//2, cy + IMG_SIZE//2), (255, 0, 0), 2)

#     # ==== Görüntüyü Göster ====
#     cv2.imshow("Garson + Yemek Sistemi", frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


import cv2
import numpy as np
import datetime
import json
import os
from pyzbar.pyzbar import decode
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

# ==== Ayarlar ====
MASA_ID = "Masa_1"
MODEL_YOLU = "yemek_modeli.h5"
LOG_DOSYASI = "loglar.json"
SINIFLAR = ['baklava', 'caesar_salad', 'chicken_wings', 'hot_and_sour_soup', 'waffles']
IMG_SIZE = 224

# ==== Model yükle ====
model = load_model(MODEL_YOLU)

# ==== Log yükle ====
if os.path.exists(LOG_DOSYASI):
    with open(LOG_DOSYASI, "r", encoding="utf-8") as f:
        loglar = json.load(f)
else:
    loglar = []

# ==== Kamera başlat ====
cap = cv2.VideoCapture(0)
print("Hazır. 'T' tuşuna basıldığında kayıt alınır.")

son_garson = None  # QR'dan gelen son garson ID

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ==== QR kodu oku (sürekli) ====
    qr_codes = decode(frame)
    for code in qr_codes:
        son_garson = code.data.decode('utf-8')
        cv2.putText(frame, f"Garson: {son_garson}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

    # ==== Görsel üzeri çizim ====
    h, w, _ = frame.shape
    cx, cy = w // 2, h // 2
    roi_rect = ((cx - IMG_SIZE//2, cy - IMG_SIZE//2), (cx + IMG_SIZE//2, cy + IMG_SIZE//2))
    cv2.rectangle(frame, roi_rect[0], roi_rect[1], (255, 0, 0), 2)

    # ==== T tuşuna basıldıysa işlem yap ====
    key = cv2.waitKey(1) & 0xFF
    if key == ord('t'):
        if son_garson is None:
            print("⚠️ Garson tanımlanmadı (QR okutulmalı)")
            continue

        # ROI al ve yemek tanı
        roi = frame[roi_rect[0][1]:roi_rect[1][1], roi_rect[0][0]:roi_rect[1][0]]
        if roi.shape[:2] != (IMG_SIZE, IMG_SIZE):
            print("⚠️ ROI boyutu uygun değil.")
            continue

        img = cv2.resize(roi, (IMG_SIZE, IMG_SIZE))
        img = img_to_array(img) / 255.0
        img = np.expand_dims(img, axis=0)

        preds = model.predict(img)[0]
        yemek = SINIFLAR[np.argmax(preds)]
        confidence = np.max(preds)

        if confidence < 0.80:
            print(f"⚠️ Tahmin düşük güvenli: {confidence:.2f}")
            continue

        # ==== Kayıt oluştur ====
        zaman = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        kayit = {
            "masa": MASA_ID,
            "garson": son_garson,
            "yemek": yemek,
            "zaman": zaman
        }

        if kayit not in loglar:
            loglar.append(kayit)
            with open(LOG_DOSYASI, "w", encoding="utf-8") as f:
                json.dump(loglar, f, indent=4, ensure_ascii=False)

        print(f"✅ {zaman} | {MASA_ID} | {son_garson} → {yemek} ✔️")

    elif key == ord('q'):
        break

    # ==== Görüntü göster ====
    cv2.imshow("Sistem: 'T' ile kayıt", frame)

cap.release()
cv2.destroyAllWindows()
