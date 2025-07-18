import json

YEMEK_FIYATLARI = {
    "baklava": 25,
    "caesar_salad": 30,
    "chicken_wings": 45,
    "hot_and_sour_soup": 20,
    "waffles": 35
}

LOG_DOSYASI = "loglar.json"

with open(LOG_DOSYASI, "r", encoding="utf-8") as f:
    loglar = json.load(f)

guncellenmis_loglar = []

for log in loglar:
    if "yemek" in log and "fiyat" not in log:
        yemek = log["yemek"]
        log["fiyat"] = YEMEK_FIYATLARI.get(yemek, 0)
    guncellenmis_loglar.append(log)

with open(LOG_DOSYASI, "w", encoding="utf-8") as f:
    json.dump(guncellenmis_loglar, f, indent=4, ensure_ascii=False)

print("✅ Fiyat bilgileri loglara eklendi.")
