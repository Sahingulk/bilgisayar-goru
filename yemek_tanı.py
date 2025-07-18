import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

# Modeli yükle
model = load_model("yemek_modeli.h5")
class_names = ['baklava', 'caesar_salad', 'chicken_wings', 'hot_and_sour_soup', 'waffles']

# Kamera başlat
cap = cv2.VideoCapture(0)

# Tahmin için bayrak
tahmin_yap = False
sonuc_text = ""

print("📸 Görüntüleme başladı. Tahmin için 's' tuşuna bas. Çıkmak için 'q'.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Odak karesi (orta alan)
    h, w, _ = frame.shape
    cx, cy = w // 2, h // 2
    size = 224
    roi = frame[cy - size//2:cy + size//2, cx - size//2:cx + size//2]

    # Ekrana bilgi yaz
    cv2.rectangle(frame, (cx - size//2, cy - size//2), (cx + size//2, cy + size//2), (255, 0, 0), 2)
    cv2.putText(frame, "Tahmin icin 's' tusuna bas", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 255, 50), 2)
    if sonuc_text:
        cv2.putText(frame, sonuc_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

    cv2.imshow("Yemek Tanima", frame)
    key = cv2.waitKey(1) & 0xFF

    # Tahmin yap
    if key == ord('s'):
        if roi.shape[0] == 224 and roi.shape[1] == 224:
            img = cv2.resize(roi, (224, 224))
            img = img_to_array(img) / 255.0
            img = np.expand_dims(img, axis=0)

            preds = model.predict(img)[0]
            predicted_label = class_names[np.argmax(preds)]
            confidence = np.max(preds)
            sonuc_text = f"{predicted_label} ({confidence*100:.1f}%)"
            print("✅ Tahmin:", sonuc_text)

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
