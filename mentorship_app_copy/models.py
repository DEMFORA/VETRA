import sqlite3
import os

conn = sqlite3.connect('mentorship.db')
cursor = conn.cursor()

# Tabloyu oluşturuyoruz
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        occupation TEXT NOT NULL,
        skills TEXT NOT NULL,
        role TEXT CHECK(role IN ('mentor', 'mentee')) NOT NULL,
        selectedMentId INTEGER REFERENCES users(id) ON DELETE SET NULL
    )
''')

# Fake verileri ekliyoruz
cursor.executemany('''
    INSERT INTO users (first_name, last_name, email, occupation, skills, role, selectedMentId)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', [
    # MENTORLER
    ("Ahmet", "Yılmaz", "ahmet.yilmaz@mail.com", "Yazılım Mühendisi", "Python", "mentor", None),
    ("Ali", "Yılmaz", "ali.yilmaz@mail.com", "Yazılım Mühendisi", "c++", "mentor", None),
    ("Kartal", "Yılmaz", "kartal.yilmaz@mail.com", "Yazılım Mühendisi", "javascript", "mentor", None),
    ("Serhat", "Yılmaz", "serhat.yilmaz@mail.com", "Yazılım Mühendisi", "Python, c++", "mentor", None),
    ("Ayşe", "Kaya", "ayse.kaya@mail.com", "Tıp Doktoru", "Kardiyoloji, Araştırma", "mentor", None),
    ("Mehmet", "Demir", "mehmet.demir@mail.com", "Mimar", "AutoCAD, Tasarım", "mentor", None),
    ("Elif", "Aydın", "elif.aydin@mail.com", "Makine Mühendisi", "SolidWorks, Termodinamik", "mentor", None),
    ("Burak", "Çelik", "burak.celik@mail.com", "Edebiyatçı", "Yaratıcı Yazarlık, Editörlük", "mentor", None),

    # MENTEELER (selectedMentId'yi mentorlarla eşleştiriyoruz)
    ("Merve", "Aksoy", "merve.aksoy@mail.com", "Bilgisayar Mühendisliği", "Python, c++", "mentee", None),  # Ahmet Yılmaz
    ("Zeynep", "Yıldız", "zeynep.yildiz@mail.com", "Üniversite Öğrencisi", "Veri Analizi", "mentee", None),
    ("Hasan", "Kurt", "hasan.kurt@mail.com", "Tıp Fakültesi Öğrencisi", "Temel Anatomi", "mentee", None),
    ("Kerem", "Şahin", "kerem.sahin@mail.com", "Mimarlık Öğrencisi", "SketchUp, Tasarım", "mentee", None),
    ("Seda", "Topal", "seda.topal@mail.com", "Psikoloji Öğrencisi", "Gelişim Psikolojisi", "mentee", None),
    ("Ege", "Kaya", "ege.kaya@mail.com", "Kimya Mühendisliği", "Organik Kimya", "mentee", None),
    ("Hilal", "Arslan", "hilal.arslan@mail.com", "Makine Mühendisliği", "CAD, CAM", "mentee", None),
    ("Umut", "Yıldırım", "umut.yildirim@mail.com", "Tıp Fakültesi", "Fizyoloji", "mentee", None),
    ("Büşra", "Polat", "busra.polat@mail.com", "Edebiyat Öğrencisi", "Modern Şiir", "mentee", None),
    ("Onur", "Koç", "onur.koc@mail.com", "Elektrik-Elektronik", "Devre Tasarımı", "mentee", None),
    ("Naz", "Güneş", "naz.gunes@mail.com", "Endüstri Mühendisliği", "Optimizasyon", "mentee", None),
    ("Emir", "Uçar", "emir.ucar@mail.com", "Biyomedikal", "Görüntüleme Sistemleri", "mentee", None),
    ("Yasemin", "Er", "yasemin.er@mail.com", "Moleküler Biyoloji", "Genetik", "mentee", None),
    ("Bora", "Şimşek", "bora.simsek@mail.com", "Matematik Öğrencisi", "Lineer Cebir", "mentee", None),
    ("Selin", "Deniz", "selin.deniz@mail.com", "Çevre Mühendisliği", "Atık Yönetimi", "mentee", None),
    ("Kaan", "Altun", "kaan.altun@mail.com", "Fizik", "Kuantum Mekaniği", "mentee", None),
    ("Melis", "Türkmen", "melis.turkmen@mail.com", "Psikoloji", "Davranış Bilimleri", "mentee", None),
    ("Tuna", "Gür", "tuna.gur@mail.com", "İstatistik", "Veri Görselleştirme", "mentee", None),
    ("Eylül", "Avcı", "eylul.avci@mail.com", "Gıda Mühendisliği", "Beslenme", "mentee", None),
])

conn.commit()
conn.close()

print("models.py çalıştı!")

if os.path.exists("mentorship.db"):
    print("✅ mentorship.db başarıyla oluşturuldu!")
else:
    print("❌ mentorship.db dosyası oluşturulamadı!")

