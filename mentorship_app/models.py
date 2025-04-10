import sqlite3
import os

conn = sqlite3.connect('mentorship.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,          -- Kullanıcının adı (ilk isim)
        last_name TEXT NOT NULL,           -- Kullanıcının soyadı
        email TEXT UNIQUE NOT NULL,        -- E-posta (benzersiz)
        occupation TEXT NOT NULL,          -- Meslek veya pozisyon
        skills TEXT NOT NULL,              -- Uzmanlık alanları (örn: Python, Veri Bilimi)
        role TEXT CHECK(role IN ('mentor', 'mentee')) NOT NULL  -- Kullanıcı rolü
    )
''')
cursor.executemany('''
    INSERT INTO users (first_name, last_name, email, occupation, skills, role)
    VALUES (?, ?, ?, ?, ?, ?)
''', [
    # MENTORLER
    ("Ahmet", "Yılmaz", "ahmet.yilmaz@example.com", "Yazılım Mühendisi", "Python, Flask", "mentor"),
    ("Ayşe", "Kaya", "ayse.kaya@example.com", "Tıp Doktoru", "Kardiyoloji, Araştırma", "mentor"),
    ("Mehmet", "Demir", "mehmet.demir@example.com", "Mimar", "AutoCAD, Tasarım", "mentor"),
    ("Elif", "Aydın", "elif.aydin@example.com", "Makine Mühendisi", "SolidWorks, Termodinamik", "mentor"),
    ("Burak", "Çelik", "burak.celik@example.com", "Edebiyatçı", "Yaratıcı Yazarlık, Editörlük", "mentor"),

    # MENTEELER
    ("Zeynep", "Yıldız", "zeynep.yildiz@example.com", "Üniversite Öğrencisi", "Veri Analizi", "mentee"),
    ("Hasan", "Kurt", "hasan.kurt@example.com", "Tıp Fakültesi Öğrencisi", "Temel Anatomi", "mentee"),
    ("Merve", "Aksoy", "merve.aksoy@example.com", "Bilgisayar Mühendisliği", "C++, Java", "mentee"),
    ("Kerem", "Şahin", "kerem.sahin@example.com", "Mimarlık Öğrencisi", "SketchUp, Tasarım", "mentee"),
    ("Seda", "Topal", "seda.topal@example.com", "Psikoloji Öğrencisi", "Gelişim Psikolojisi", "mentee"),
    ("Ege", "Kaya", "ege.kaya@example.com", "Kimya Mühendisliği", "Organik Kimya", "mentee"),
    ("Hilal", "Arslan", "hilal.arslan@example.com", "Makine Mühendisliği", "CAD, CAM", "mentee"),
    ("Umut", "Yıldırım", "umut.yildirim@example.com", "Tıp Fakültesi", "Fizyoloji", "mentee"),
    ("Büşra", "Polat", "busra.polat@example.com", "Edebiyat Öğrencisi", "Modern Şiir", "mentee"),
    ("Onur", "Koç", "onur.koc@example.com", "Elektrik-Elektronik", "Devre Tasarımı", "mentee"),
    ("Naz", "Güneş", "naz.gunes@example.com", "Endüstri Mühendisliği", "Optimizasyon", "mentee"),
    ("Emir", "Uçar", "emir.ucar@example.com", "Biyomedikal", "Görüntüleme Sistemleri", "mentee"),
    ("Yasemin", "Er", "yasemin.er@example.com", "Moleküler Biyoloji", "Genetik", "mentee"),
    ("Bora", "Şimşek", "bora.simsek@example.com", "Matematik Öğrencisi", "Lineer Cebir", "mentee"),
    ("Selin", "Deniz", "selin.deniz@example.com", "Çevre Mühendisliği", "Atık Yönetimi", "mentee"),
    ("Kaan", "Altun", "kaan.altun@example.com", "Fizik", "Kuantum Mekaniği", "mentee"),
    ("Melis", "Türkmen", "melis.turkmen@example.com", "Psikoloji", "Davranış Bilimleri", "mentee"),
    ("Tuna", "Gür", "tuna.gur@example.com", "İstatistik", "Veri Görselleştirme", "mentee"),
    ("Eylül", "Avcı", "eylul.avci@example.com", "Gıda Mühendisliği", "Beslenme", "mentee")
])


conn.commit()
conn.close()

print("models.py çalıştı!")

if os.path.exists("mentorship.db"):
    print("✅ mentorship.db başarıyla oluşturuldu!")
else:
    print("❌ mentorship.db dosyası oluşturulamadı!")
