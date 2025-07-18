import qrcode

# QR kodlara yazılacak veriler
garsonlar = {
    "Garson_1": "Garson_1",
    "Garson_2": "Garson_2"
}

for isim, veri in garsonlar.items():
    img = qrcode.make(veri)
    img.save(f"{isim}.png")  # Örneğin: Garson_1.png
    print(f"{isim} için QR kod oluşturuldu.")
