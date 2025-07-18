import json
from datetime import datetime, timedelta

LOG_DOSYASI = "loglar.json"
SON_SIFIRLAMALAR = {}  # {"Masa_1": datetime objesi}

def hesap_sifirla(masa):
    simdi = datetime.now()

    if masa in SON_SIFIRLAMALAR:
        fark = simdi - SON_SIFIRLAMALAR[masa]
        if fark.total_seconds() < 10:
            print(f"⚠️ {masa} için zaten yakın zamanda sıfırlama yapılmış!")
            return

    SON_SIFIRLAMALAR[masa] = simdi

    yeni_log = {
        "masa": masa,
        "zaman": simdi.strftime("%Y-%m-%d %H:%M:%S"),
        "hesap_sifirla": True
    }

    try:
        with open(LOG_DOSYASI, "r", encoding="utf-8") as f:
            loglar = json.load(f)
    except FileNotFoundError:
        loglar = []

    loglar.append(yeni_log)

    with open(LOG_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(loglar, f, indent=4, ensure_ascii=False)

    print(f"✅ {masa} için hesap sıfırlandı! ({yeni_log['zaman']})")


# Simülasyon: QR okutulunca masa adı geliyor
while True:
    masa = input("QR kod okundu (örnek: Masa_1): ").strip()
    if masa:
        hesap_sifirla(masa)
