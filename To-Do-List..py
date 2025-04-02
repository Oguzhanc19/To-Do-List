import datetime
import os
import colorama

colorama.init()

RED = colorama.Fore.RED
BLUE = colorama.Fore.CYAN
GREEN = colorama.Fore.GREEN
RESET = colorama.Fore.RESET

def gorevleri_listele(gorevler, filtre=None):
    if not gorevler:
        print("\nGörev listesi boş.")
        return

    filtrelenmis_gorevler = gorevler
    if filtre:
        filtrelenmis_gorevler = [
            (gorev, tarih, durum, oncelik, son_tarih)
            for gorev, tarih, durum, oncelik, son_tarih in gorevler
            if (filtre == "tamamlandi" and durum) or (filtre == "tamamlanmadi" and not durum)
        ]

    if not filtrelenmis_gorevler:
        if filtre == "tamamlandi":
            print("\nHenüz tamamlanmış bir görev bulunmamaktadır.")
        elif filtre == "tamamlanmadi":
            if all(durum for _, _, durum, _, _ in gorevler):  # Tüm görevler tamamlanmış mı kontrolü
                print("\nTüm görevler başarıyla tamamlanmıştır, tebrikler!")
            else:
                print("Henüz tamamlanmamış bir görev bulunmamaktadır.")  # Filtrelenmiş liste boşsa
        return  # Fonksiyondan çık

    for i, (gorev, tarih, durum, oncelik, son_tarih) in enumerate(filtrelenmis_gorevler):
        durum_str = "✓" if durum else "✗"
        oncelik_renk = RED if oncelik == 3 else BLUE if oncelik == 2 else GREEN
        oncelik_str = "*" * oncelik

        print(f"\n{i+1}. {gorev}")
        print(f"Eklenme Tarihi: {tarih}")
        print(f"Durum: {durum_str}")
        print(f"Öncelik: {oncelik_renk}{oncelik_str}{RESET}")
        if son_tarih:
            print(f"Son Tarih: {son_tarih}")
        print("-" * 20)

def gorev_ara(gorevler):
    """Görevi adına veya açıklamasına göre arama yapar."""
    aranan_kelime = input("Aranacak kelimeyi girin: ").lower()
    bulunan_gorevler = []
    for i, (gorev, tarih, durum, oncelik, son_tarih) in enumerate(gorevler):
        if aranan_kelime in gorev.lower():
            bulunan_gorevler.append((gorev, tarih, durum, oncelik, son_tarih))

    if bulunan_gorevler:
        print("\nBulunan Görevler:")
        gorevleri_listele(bulunan_gorevler) # Bulunan görevleri listele
    else:
        print("Aranan kelimeye uygun görev bulunamadı.")

def yeni_gorev_ekle(gorevler):
        """Yeni bir görev ekler."""
        yeni_gorev = input("Yeni görevi girin: ")
        if not yeni_gorev.strip():
            print("Boş görev eklenemez.")
            return

        eklenme_tarihi = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        durum = False
        oncelik = input(
            "Öncelik seviyesini girin (1-Düşük, 2-Orta, 3-Yüksek): ")
        try:
            oncelik = int(oncelik)
            if oncelik not in [1, 2, 3]:
                raise ValueError
        except ValueError:
            print("Geçersiz öncelik seviyesi. Varsayılan olarak 'Orta' ayarlanıyor.")
            oncelik = 2

        while True:  # Tarih kontrol döngüsü
            try:
                son_tarih_str = input("Son tarihi girin (YYYY-MM-DD): ")
                son_tarih = datetime.datetime.strptime(
                    son_tarih_str, "%Y-%m-%d").date()
                if son_tarih < datetime.date.today():
                    print(
                        "Son tarih, bugünden önceki bir tarih olamaz. Lütfen tekrar girin.")
                else:
                    break  # Doğru tarih girildiğinde döngüden çık
            except ValueError:
                print("Geçersiz tarih formatı. Lütfen YYYY-MM-DD formatında girin.")

        gorevler.append((yeni_gorev, eklenme_tarihi,
                        durum, oncelik, son_tarih))
        print("Görev eklendi.")

def gorev_duzenle(gorevler):
        """Belirtilen görevi düzenler."""
        gorevleri_listele(gorevler)
        if not gorevler:
            return

        try:
            gorev_no = int(
                input("Düzenlemek istediğiniz görevin numarasını girin: ")) - 1
            if not (0 <= gorev_no < len(gorevler)):
                raise IndexError  # Geçersiz görev numarası için IndexError oluştur

            gorev, tarih, durum, oncelik, son_tarih = gorevler[gorev_no]

            while True:
                print("\nNeyi düzenlemek istersiniz?")
                print("1. Mesaj")
                print("2. Son Tarih")
                print("3. Tamamlanma Durumu")
                print("4. Öncelik")
                print("5. İptal")

                secim = input("Seçiminizi yapın: ")

                if secim == "1":
                    yeni_mesaj = input("Yeni mesajı girin: ")
                    gorevler[gorev_no] = (
                        yeni_mesaj, tarih, durum, oncelik, son_tarih)
                    print("Mesaj güncellendi.")
                    break
                elif secim == "2":
                    while True:
                        try:
                            yeni_son_tarih_str = input(
                                "Yeni son tarihi girin (YYYY-MM-DD): ")
                            yeni_son_tarih = datetime.datetime.strptime(
                                yeni_son_tarih_str, "%Y-%m-%d").date()
                            if yeni_son_tarih < datetime.date.today():
                                print(
                                    "Son tarih, bugünden önceki bir tarih olamaz. Lütfen tekrar girin.")
                            else:
                                gorevler[gorev_no] = (
                                    gorev, tarih, durum, oncelik, yeni_son_tarih)
                                print("Son tarih güncellendi.")
                                break
                        except ValueError:
                            print(
                                "Geçersiz tarih formatı. Lütfen YYYY-MM-DD formatında girin.")
                    break
                elif secim == "3":
                    yeni_durum = input("Tamamlandı mı? (e/h): ").lower() == "e"
                    gorevler[gorev_no] = (
                        gorev, tarih, yeni_durum, oncelik, son_tarih)
                    print("Tamamlanma durumu güncellendi.")
                    break
                elif secim == "4":
                    while True:
                        try:
                            yeni_oncelik = int(
                                input("Yeni öncelik seviyesini girin (1-Düşük, 2-Orta, 3-Yüksek): "))
                            if 1 <= yeni_oncelik <= 3:
                                gorevler[gorev_no] = (
                                    gorev, tarih, durum, yeni_oncelik, son_tarih)
                                print("Öncelik güncellendi.")
                                break
                            else:
                                print(
                                    "Geçersiz öncelik seviyesi. Lütfen 1, 2 veya 3 girin.")
                        except ValueError:
                            print("Geçersiz giriş. Lütfen bir sayı girin.")
                    break

                elif secim == "5":
                    print("Düzenleme iptal edildi.")
                    break
                else:
                    print("Geçersiz seçim. Lütfen tekrar deneyin.")

        except ValueError:
            print("Geçersiz giriş. Lütfen bir sayı girin.")
        except IndexError:
            print("Geçersiz görev numarası.")

def gorev_sil(gorevler):
        """Belirtilen görevi siler."""
        gorevleri_listele(gorevler)
        if not gorevler:
            return

        try:
            gorev_no = int(
                input("Silmek istediğiniz görevin numarasını girin: ")) - 1
            if 0 <= gorev_no < len(gorevler):
                del gorevler[gorev_no]
                print("Görev silindi.")
            else:
                print("Geçersiz görev numarası.")
        except ValueError:
            print("Geçersiz giriş. Lütfen bir sayı girin.")
        except IndexError:
            print("Geçersiz görev numarası.")

def gorevleri_kaydet(gorevler, dosya_adi="gorevler.txt"):
        try:
            with open(dosya_adi, "w", encoding="utf-8") as dosya:
                for gorev, tarih, durum, oncelik, son_tarih in gorevler:
                    son_tarih_str = son_tarih.strftime(
                        "%Y-%m-%d") if son_tarih else ""
                    dosya.write(f"{gorev}|{tarih}|{durum}|{
                                oncelik}|{son_tarih_str}\n")
        except OSError as e:
            print(f"Dosya yazma hatası: {e}")

def gorevleri_yukle(dosya_adi="gorevler.txt"):
        gorevler = []
        try:
            with open(dosya_adi, "r", encoding="utf-8") as dosya:
                for satir in dosya:
                    gorev, tarih_str, durum_str, oncelik_str, son_tarih_str = satir.strip().split("|")
                    tarih = datetime.datetime.strptime(
                        tarih_str, "%Y-%m-%d %H:%M:%S")
                    durum = durum_str.lower() == "true"
                    oncelik = int(oncelik_str)
                    son_tarih = datetime.datetime.strptime(
                        son_tarih_str, "%Y-%m-%d").date() if son_tarih_str else None
                    gorevler.append((gorev, tarih, durum, oncelik, son_tarih))
        except FileNotFoundError:
            print("Görev dosyası bulunamadı. Yeni bir dosya oluşturulacak.")
        except OSError as e:
            print(f"Dosya okuma hatası: {e}")
        except (ValueError, IndexError):  # Split hatası veya veri dönüştürme hatası
            print("Görev dosyası bozuk. Yeni bir dosya oluşturulacak.")
            gorevler = []  # Bozuk verileri temizle
        return gorevler

def main():
        dosya_adi = "gorevler.txt"
        gorevler = gorevleri_yukle(dosya_adi)
        degisiklik_yapildi = False

        while True:
            print("\nTo-Do-List\n")
            print("Ana Menü:\n")
            print("1. Görevleri Listele")
            print("2. Yeni Görev Ekle")
            print("3. Görev Düzenle")
            print("4. Görev Sil")
            print("5. Görev Ara")
            print("6. Çıkış")

            secim = input("\nSeçiminizi yapın: ")
           
            if secim == "1":
                while True:
                    print("\nFiltreleme Seçenekleri:")
                    print("1. Tüm Görevler")
                    print("2. Tamamlanan Görevler")
                    print("3. Tamamlanmamış Görevler")
                    print("4. Geri")
    
                    filtre_secim = input("Seçiminizi yapın: ")
    
                    if filtre_secim == "1":
                        gorevleri_listele(gorevler)
                        break
                    elif filtre_secim == "2":
                        gorevleri_listele(gorevler, filtre="tamamlandi")
                        break
                    elif filtre_secim == "3":
                        gorevleri_listele(gorevler, filtre="tamamlanmadi")
                        break
                    elif filtre_secim == "4":
                        break
                    else:
                        print("Geçersiz seçim. Lütfen tekrar deneyin.")

            elif secim == "2":
                yeni_gorev_ekle(gorevler)
                degisiklik_yapildi = True
                
            elif secim == "3":
                gorev_duzenle(gorevler)
                degisiklik_yapildi = True
            elif secim == "4":
                gorev_sil(gorevler)
                degisiklik_yapildi = True
            elif secim == "5":  # Çıkış seçeneği
                gorev_ara(gorevler)
            elif secim == "6": # Arama için yeni seçenek
                if degisiklik_yapildi:
                    while True:
                        kaydet_secim = input(
                            "Değişiklikleri kaydetmek istiyor musunuz? (e/h): ").lower()
                        if kaydet_secim == "e":
                            gorevleri_kaydet(gorevler, dosya_adi)
                            print("Görevler kaydedildi.")
                            break
                        elif kaydet_secim == "h":
                            print("Değişiklikler kaydedilmedi.")
                            break
                        else:
                            print("Geçersiz seçim. Lütfen 'e' veya 'h' girin.")
                print("\nÇıkış yapılıyor...\n")
                break
                
            else:
                print("\nGeçersiz seçim. Lütfen tekrar deneyin.\n")

if __name__ == "__main__":
        main()
