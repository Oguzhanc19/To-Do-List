<div align="center">
  <h1>📋 Python To-Do List Manager</h1>
  <p><i>Command-Line Task Tracking Application<br>Komut Satırı Görev Takip Uygulaması</i></p>
  ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
</div>

<br>

## 🇬🇧 English

A minimalist yet highly effective Command-Line Interface (CLI) application for task management, written in Python. It demonstrates fundamental CRUD (Create, Read, Update, Delete) operations interacting with local memory or files.

### 🧠 Logic Execution
- **State Array**: Tasks are temporarily stored in a dynamic Python list. 
- **Infinite Loop Architecture**: The application operates inside a `while True` loop, presenting a menu to the user continuously until they explicitly choose the "Exit" command.
- **Index Management**: When users delete or update a task, the script validates the list index mathematically to avoid `IndexError` exceptions.

---

## 🇹🇷 Türkçe

Görev yönetimi için Python ile yazılmış, minimalist ancak oldukça etkili bir Komut Satırı Arayüzü (CLI) uygulamasıdır. Yerel bellek (veya dosyalar) ile etkileşime girerek temel CRUD (Oluştur, Oku, Güncelle, Sil) operasyonlarının nasıl yapıldığını gösterir.

### 🧠 Mantıksal İşleyiş
- **Durum Dizisi (State Array)**: Görevler (task) Python'un dinamik listelerinde (array) geçici olarak tutulur.
- **Sonsuz Döngü Mimarisi (Infinite Loop)**: Uygulama bir `while True` döngüsü içinde çalışır. Kullanıcı "Çıkış" komutunu girene kadar menü tekrar tekrar ekrana basılır.
- **İndeks Yönetimi**: Kullanıcı bir görevi silmek veya güncellemek istediğinde, betik girilen numarayı listenin uzunluğu ile matematiksel olarak kıyaslayarak `IndexError` (liste sınırı aşımı) hatalarını engeller.
