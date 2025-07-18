import json
from collections import defaultdict
from datetime import datetime

LOG_DOSYASI = "loglar.json"

# Fiyat bilgileri
YEMEK_FIYATLARI = {
    "baklava": 25,
    "caesar_salad": 30,
    "chicken_wings": 45,
    "hot_and_sour_soup": 20,
    "waffles": 35
}

with open(LOG_DOSYASI, "r", encoding="utf-8") as f:
    loglar = json.load(f)

garson_raporu = defaultdict(lambda: {
    "toplam_yemek": 0,
    "masalar": set(),
    "gec_kalma_sayisi": 0,
    "toplam_tutar": 0,
    "yemekler": defaultdict(int)
})

gunluk_rapor = defaultdict(list)
masa_hesaplari = defaultdict(float)
masa_son_sifirlama = {}

for log in loglar:
    garson = log.get("garson", "Belirsiz")
    masa = log.get("masa", "Bilinmiyor")
    zaman = datetime.strptime(log["zaman"], "%Y-%m-%d %H:%M:%S")
    tarih = log["zaman"].split()[0]
    gunluk_rapor[tarih].append(log)

    if log.get("hesap_sifirla"):
        masa_son_sifirlama[masa] = zaman
        continue

    if log.get("gec_kalma"):
        garson_raporu[garson]["gec_kalma_sayisi"] += 1
        continue

    if "yemek" in log:
        if masa in masa_son_sifirlama and zaman <= masa_son_sifirlama[masa]:
            continue

        yemek = log["yemek"]
        fiyat = log.get("fiyat") or YEMEK_FIYATLARI.get(yemek, 0)

        garson_raporu[garson]["toplam_yemek"] += 1
        garson_raporu[garson]["masalar"].add(masa)
        garson_raporu[garson]["toplam_tutar"] += fiyat
        garson_raporu[garson]["yemekler"][yemek] += 1

        masa_hesaplari[masa] += fiyat

# ---- Terminal çıktısı ----
print("📋 GARSON PERFORMANS RAPORU")
for garson, veri in garson_raporu.items():
    print(f"\n🧍 {garson}")
    print(f"  🍽️ Toplam yemek: {veri['toplam_yemek']}")
    print(f"  💰 Toplam ciro: {veri['toplam_tutar']} TL")
    print(f"  🪑 Hizmet verdiği masalar: {', '.join(veri['masalar'])}")
    print(f"  ⏱️ Geç kalma: {veri['gec_kalma_sayisi']} kez")
    print("  🍲 Yemek dağılımı:")
    for yemek, adet in veri["yemekler"].items():
        print(f"    - {yemek}: {adet} kez")

print("\n📅 GÜNLÜK RAPORLAR")
for tarih, kayitlar in gunluk_rapor.items():
    print(f"- {tarih}: {len(kayitlar)} işlem")

print("\n💵 MASA BAZLI HESAPLAR")
for masa, tutar in masa_hesaplari.items():
    print(f"  {masa}: {tutar} TL")

# ---- JSON rapor dosyası ----
rapor_json = {
    "garson_raporu": {
        g: {
            "toplam_yemek": v["toplam_yemek"],
            "masalar": list(v["masalar"]),
            "gec_kalma_sayisi": v["gec_kalma_sayisi"],
            "toplam_tutar": v["toplam_tutar"],
            "yemekler": dict(v["yemekler"])
        }
        for g, v in garson_raporu.items()
    },
    "gunluk_rapor": gunluk_rapor,
    "masa_hesaplari": dict(masa_hesaplari)
}

with open("rapor.json", "w", encoding="utf-8") as f:
    json.dump(rapor_json, f, indent=4, ensure_ascii=False)

print("\n📄 rapor.json dosyası oluşturuldu ✔️")
