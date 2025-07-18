import qrcode

# Masa için özel QR metni
qr_verisi = "HESAP_SIFIRLA:Masa_1"

# QR kod üret
qr = qrcode.make(qr_verisi)

# Dosyayı kaydet
qr.save("hesap_sifirla_masa1.png")

print("✅ hesap_sifirla_masa1.png oluşturuldu")
