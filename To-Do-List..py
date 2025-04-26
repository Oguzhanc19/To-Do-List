# Yaptığım bu projede bir çok farklı özellik bulunmaktadır. Kullanıcılar görev ekleyebilir, düzenleyebilir, silebilir ve görevleri listeleyebilir. 
# Görevler tamamlanma durumuna göre filtrelenebilir ve arama yapılabilir. Görevler bir dosyaya kaydedilir ve uygulama başlatıldığında bu dosyadan yüklenir.
# Proje, kullanıcı dostu bir arayüz sunarak görev yönetimini kolaylaştırmayı amaçlamaktadır.
# Bu projenin diğerinden bir farkı da görsel arayüz içermesi.

import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime

#Öncelikle arayüz tasarımını yaptım
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.gorevler = self.gorevleri_yukle()  # Görevleri dosyadan yükle

        # Ana çerçeve
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        # Görev listesi
        self.gorev_listbox = tk.Listbox(self.frame, width=50, height=15)
        self.gorev_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        # Kaydırma çubuğu
        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.gorev_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.gorev_listbox.yview)

        # Düğmeler
        self.add_button = tk.Button(root, text="Yeni Görev Ekle", command=self.yeni_gorev_ekle)
        self.add_button.pack(pady=5)

        self.edit_button = tk.Button(root, text="Görev Düzenle", command=self.gorev_duzenle)
        self.edit_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Görev Sil", command=self.gorev_sil)
        self.delete_button.pack(pady=5)

        self.show_all_button = tk.Button(root, text="Tüm Görevleri Listele", command=lambda: self.load_gorevler())
        self.show_all_button.pack(pady=5)

        self.show_completed_button = tk.Button(root, text="Tamamlanan Görevleri Göster", command=lambda: self.load_gorevler(filtre="tamamlandi"))
        self.show_completed_button.pack(pady=5)

        self.show_incomplete_button = tk.Button(root, text="Tamamlanmamış Görevleri Göster", command=lambda: self.load_gorevler(filtre="tamamlanmadi"))
        self.show_incomplete_button.pack(pady=5)

        self.search_button = tk.Button(root, text="Görev Ara", command=self.gorev_ara)
        self.search_button.pack(pady=5)

        self.sort_priority_button = tk.Button(root, text="Önceliğe Göre Sırala", command=lambda: self.load_gorevler(sirala="oncelik"))
        self.sort_priority_button.pack(pady=5)

        self.sort_date_button = tk.Button(root, text="Tarihe Göre Sırala", command=lambda: self.load_gorevler(sirala="tarih"))
        self.sort_date_button.pack(pady=5)

        self.save_button = tk.Button(root, text="Kaydet", command=self.gorevleri_kaydet)
        self.save_button.pack(pady=5)

        self.load_gorevler()  
        
    #Bu kısımda da görevleri filtreleyebildiğimiz özellikler ekledim
    def load_gorevler(self, filtre=None, sirala=None):
        """Görevleri listbox'a yükler, isteğe bağlı olarak filtre uygular ve sıralar."""
        self.gorev_listbox.delete(0, tk.END)
        sorted_gorevler = self.gorevler

        if sirala == "oncelik":
            sorted_gorevler = sorted(self.gorevler, key=lambda x: x[3], reverse=True)  # Önceliğe göre sırala
        elif sirala == "tarih":
            sorted_gorevler = sorted(self.gorevler, key=lambda x: x[4] if x[4] else datetime.date.max)  # Tarihe göre sırala

        for gorev, tarih, durum, oncelik, son_tarih in sorted_gorevler:
            if filtre == "tamamlandi" and not durum:
                continue
            if filtre == "tamamlanmadi" and durum:
                continue
            durum_str = "✓" if durum else "✗"
            oncelik_str = "*" * oncelik
            self.gorev_listbox.insert(tk.END, f"{gorev} - {durum_str} - {oncelik_str} - {son_tarih}")
            
    #Yeni görev eklemek için kullandığım fonksiyon
    def yeni_gorev_ekle(self):
        """Yeni bir görev ekler."""
        yeni_gorev = simpledialog.askstring("Yeni Görev", "Görev adını girin:")
        if yeni_gorev:
            eklenme_tarihi = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            durum = False
            oncelik = simpledialog.askinteger("Öncelik", "Öncelik seviyesini girin (1-Düşük, 2-Orta, 3-Yüksek):", minvalue=1, maxvalue=3)
            son_tarih_str = simpledialog.askstring("Son Tarih", "Son tarihi girin (YYYY-MM-DD):")
            try:
                son_tarih = datetime.datetime.strptime(son_tarih_str, "%Y-%m-%d").date()
                if son_tarih < datetime.date.today():
                    messagebox.showerror("Hata", "Son tarih bugünden önce olamaz.")
                    return
            except ValueError:
                messagebox.showerror("Hata", "Geçersiz tarih formatı.")
                return

            self.gorevler.append((yeni_gorev, eklenme_tarihi, durum, oncelik, son_tarih))
            self.load_gorevler()
            
    #Görevleri düzenlememizi sağlayan fonksiyon ekledim     
    def gorev_duzenle(self):
        """Seçili görevi düzenler."""
        selected_index = self.gorev_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Uyarı", "Lütfen bir görev seçin.")
            return

        index = selected_index[0]
        gorev, tarih, durum, oncelik, son_tarih = self.gorevler[index]

        while True:
            secim = simpledialog.askinteger("Düzenle", "Neyi düzenlemek istersiniz?\n1. Mesaj\n2. Son Tarih\n3. Tamamlanma Durumu\n4. Öncelik\n5. İptal", minvalue=1, maxvalue=5)
            if secim == 1:
                yeni_mesaj = simpledialog.askstring("Mesaj Düzenle", "Yeni mesajı girin:", initialvalue=gorev)
                if yeni_mesaj:
                    self.gorevler[index] = (yeni_mesaj, tarih, durum, oncelik, son_tarih)
            elif secim == 2:
                yeni_son_tarih_str = simpledialog.askstring("Son Tarih Düzenle", "Yeni son tarihi girin (YYYY-MM-DD):", initialvalue=son_tarih.strftime("%Y-%m-%d"))
                try:
                    yeni_son_tarih = datetime.datetime.strptime(yeni_son_tarih_str, "%Y-%m-%d").date()
                    if yeni_son_tarih < datetime.date.today():
                        messagebox.showerror("Hata", "Son tarih bugünden önce olamaz.")
                        continue
                    self.gorevler[index] = (gorev, tarih, durum, oncelik, yeni_son_tarih)
                except ValueError:
                    messagebox.showerror("Hata", "Geçersiz tarih formatı.")
                    continue
            elif secim == 3:
                yeni_durum = messagebox.askyesno("Durum Düzenle", "Görev tamamlandı mı?")
                self.gorevler[index] = (gorev, tarih, yeni_durum, oncelik, son_tarih)
            elif secim == 4:
                yeni_oncelik = simpledialog.askinteger("Öncelik Düzenle", "Yeni öncelik seviyesini girin (1-Düşük, 2-Orta, 3-Yüksek):", initialvalue=oncelik, minvalue=1, maxvalue=3)
                if yeni_oncelik:
                    self.gorevler[index] = (gorev, tarih, durum, yeni_oncelik, son_tarih)
            elif secim == 5:
                break
            self.load_gorevler()
            break
    #İstenmeyen veya biten görevleri silmek için bir silme fonksiyonu ekledim
    def gorev_sil(self):
        """Seçili görevi siler."""
        selected_index = self.gorev_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Uyarı", "Lütfen bir görev seçin.")
            return

        index = selected_index[0]
        del self.gorevler[index]
        self.load_gorevler()
    
    #Kullanıcının görevleri daha rahat görebilmesi için onları içeriğine göre arama özelliği ekledim.
    def gorev_ara(self):
        """Görevleri arar."""
        aranan_kelime = simpledialog.askstring("Görev Ara", "Aranacak kelimeyi girin:")
        if aranan_kelime:
            self.gorev_listbox.delete(0, tk.END)
            bulundu = False
            for gorev, tarih, durum, oncelik, son_tarih in self.gorevler:
                if aranan_kelime.lower() in gorev.lower():
                    bulundu = True
                    durum_str = "✓" if durum else "✗"
                    oncelik_str = "*" * oncelik
                    self.gorev_listbox.insert(tk.END, f"{gorev} - {durum_str} - {oncelik_str} - {son_tarih}")
            if not bulundu:
                messagebox.showinfo("Sonuç", "Böyle bir görev yok.")
                
    #Görevleri bir .txt dosyasına döüştürüp ayrıca bilgisayarda tutan fonksiyon da ekledim.
    def gorevleri_yukle(self, dosya_adi="gorevler.txt"):
        """Görevleri belirtilen dosyadan yükler."""
        gorevler = []
        try:
            with open(dosya_adi, "r", encoding="utf-8") as dosya:
                for satir in dosya:
                    gorev, tarih_str, durum_str, oncelik_str, son_tarih_str = satir.strip().split("|")
                    tarih = datetime.datetime.strptime(tarih_str, "%Y-%m-%d %H:%M:%S")
                    durum = durum_str == "tamamlandı"
                    oncelik = {"düşük": 1, "orta": 2, "yüksek": 3}[oncelik_str]
                    son_tarih = datetime.datetime.strptime(son_tarih_str, "%Y-%m-%d").date() if son_tarih_str else None
                    gorevler.append((gorev, tarih, durum, oncelik, son_tarih))
        except FileNotFoundError:
            print("Görev dosyası bulunamadı. Yeni bir dosya oluşturulacak.")
        except OSError as e:
            print(f"Dosya okuma hatası: {e}")
        except (ValueError, IndexError):  # Split hatası veya veri dönüştürme hatası
            print("Görev dosyası bozuk. Yeni bir dosya oluşturulacak.")
            gorevler = []  # Bozuk verileri temizle
        return gorevler
    
    #Görevleri uygulamadan çıkarken kaydetmek için veya tuşa basarak kaydetmek için bir fonksiyon
    def gorevleri_kaydet(self, dosya_adi="gorevler.txt"):
        """Görevleri belirtilen dosyaya kaydeder."""
        try:
            with open(dosya_adi, "w", encoding="utf-8") as dosya:
                for gorev, tarih, durum, oncelik, son_tarih in self.gorevler:
                    durum_str = "tamamlandı" if durum else "tamamlanmadı"
                    oncelik_str = {1: "düşük", 2: "orta", 3: "yüksek"}[oncelik]
                    son_tarih_str = son_tarih.strftime("%Y-%m-%d") if son_tarih else ""
                    dosya.write(f"{gorev}|{tarih}|{durum_str}|{oncelik_str}|{son_tarih_str}\n")
            messagebox.showinfo("Başarılı", "Görevler başarıyla kaydedildi.")
        except OSError as e:
            print(f"Dosya yazma hatası: {e}")
            
    def on_closing(self):
        """Uygulama kapanırken görevleri kaydeder."""
        self.gorevleri_kaydet()  # Program kapanırken otomatik kaydet
        if messagebox.askokcancel("Çıkış", "Çıkmak istediğinizden emin misiniz?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
