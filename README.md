# 📝 To-Do List Uygulaması

Bu proje, **Python (Tkinter)** kullanılarak geliştirilmiş bir **görsel arayüzlü To-Do List uygulamasıdır**.  
Kullanıcıların görevlerini ekleyebileceği, düzenleyebileceği, silebileceği, arayabileceği ve filtreleyebileceği basit ve işlevsel bir görev yönetim sistemidir.  
Görevler ayrıca bir dosyaya kaydedilir ve uygulama yeniden başlatıldığında dosyadan yüklenir.

---

## 🚀 Özellikler

- ✅ Yeni görev ekleme  
- ✏️ Görev düzenleme  
- 🗑️ Görev silme  
- 📋 Tüm görevleri listeleme  
- 🎯 Tamamlanan / tamamlanmamış görevleri filtreleme  
- 🔍 Anahtar kelime ile görev arama  
- 📅 Görevleri **tarihe** veya **önceliğe** göre sıralama  
- 💾 Görevleri `gorevler.txt` dosyasına kaydetme ve uygulama açıldığında yükleme  
- 🖥️ Kullanıcı dostu **Tkinter tabanlı görsel arayüz**

---

## 📂 Proje Yapısı

ToDoApp

├── todo.py # Ana uygulama kodu

├── gorevler.txt # Görevlerin kaydedildiği dosya (otomatik oluşturulur)

└── README.md # Proje açıklamaları


---

## ⚙️ Gereksinimler

- Python 3.8+
- Tkinter (Python ile birlikte gelir, ayrıca yüklemenize gerek yok)

---

## ▶️ Kurulum ve Çalıştırma

1. Projeyi bilgisayarınıza indirin veya kopyalayın:
   ```bash
   git clone https://github.com/kullaniciadi/ToDoApp.git
   cd ToDoApp

Uygulamayı başlatın:
```bash
python todo.py
```

## 📖 Kullanım Detayları

Yeni Görev Ekle → Görev adı, öncelik (1-3 arası) ve son tarih girilir.

Görev Düzenle → Seçilen görev üzerinde mesaj, tarih, tamamlanma durumu veya öncelik değiştirilebilir.

Görev Sil → Seçilen görev listeden kaldırılır.

Görev Ara → Girilen kelimeyi içeren görevler filtrelenerek gösterilir.

Kaydet → Tüm görevler gorevler.txt dosyasına kaydedilir.

Çıkış → Uygulama kapanırken otomatik kaydedilir.
