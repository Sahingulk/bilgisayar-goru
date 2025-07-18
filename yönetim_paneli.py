import os
import subprocess

def calistir(script_adi):
    if os.path.exists(script_adi):
        subprocess.run(["python", script_adi])
    else:
        print(f"❌ {script_adi} bulunamadı!")

def menu():
    while True:
        print("\n🔧 Yönetim Paneli")
        print("1️⃣  Garson Tanıma (QR ile)")
        print("2️⃣  Hesap Sıfırlama (QR ile)")
        print("3️⃣  Yemek Tanıma (Kamera ile)")
        print("4️⃣  Raporları Görüntüle")
        print("5️⃣  Çıkış")

        secim = input("Seçiminiz (1-5): ")

        if secim == "1":
            calistir("qr_masa_kayit.py")
        elif secim == "2":
            calistir("qr_hesap_sifirla.py")
        elif secim == "3":
            calistir("yemek_tanı.py")  # Bu dosyanın ismi sende farklıysa düzelt
        elif secim == "4":
            calistir("rapor_olustur.py")
        elif secim == "5":
            print("👋 Çıkılıyor...")
            break
        else:
            print("❌ Geçersiz seçim. Lütfen 1-5 arasında bir sayı girin.")

if __name__ == "__main__":
    menu()
