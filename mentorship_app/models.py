import sqlite3
import os

conn = sqlite3.connect('mentorship.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        occupation TEXT NOT NULL,
        skills TEXT NOT NULL,
        role TEXT CHECK(role IN ('mentor', 'mentee')) NOT NULL
    )
''')

cursor.executemany('''
    INSERT INTO users (first_name, last_name, email, occupation, skills, role)
    VALUES (?, ?, ?, ?, ?, ?)
''', [
    # MENTORLER
    ("Ahmet", "Yılmaz", "ahmet.yilmaz@mail.com", "Yazılım Mühendisi", "Python, Flask", "mentor"),
    ("Ayşe", "Kaya", "ayse.kaya@mail.com", "Tıp Doktoru", "Kardiyoloji, Araştırma", "mentor"),
    ("Mehmet", "Demir", "mehmet.demir@mail.com", "Mimar", "AutoCAD, Tasarım", "mentor"),
    ("Elif", "Aydın", "elif.aydin@mail.com", "Makine Mühendisi", "SolidWorks, Termodinamik", "mentor"),
    ("Burak", "Çelik", "burak.celik@mail.com", "Edebiyatçı", "Yaratıcı Yazarlık, Editörlük", "mentor"),

    # MENTEELER
    ("Zeynep", "Yıldız", "zeynep.yildiz@mail.com", "Üniversite Öğrencisi", "Veri Analizi", "mentee"),
    ("Hasan", "Kurt", "hasan.kurt@mail.com", "Tıp Fakültesi Öğrencisi", "Temel Anatomi", "mentee"),
    ("Merve", "Aksoy", "merve.aksoy@mail.com", "Bilgisayar Mühendisliği", "C++, Java", "mentee"),
    ("Kerem", "Şahin", "kerem.sahin@mail.com", "Mimarlık Öğrencisi", "SketchUp, Tasarım", "mentee"),
    ("Seda", "Topal", "seda.topal@mail.com", "Psikoloji Öğrencisi", "Gelişim Psikolojisi", "mentee"),
    ("Ege", "Kaya", "ege.kaya@mail.com", "Kimya Mühendisliği", "Organik Kimya", "mentee"),
    ("Hilal", "Arslan", "hilal.arslan@mail.com", "Makine Mühendisliği", "CAD, CAM", "mentee"),
    ("Umut", "Yıldırım", "umut.yildirim@mail.com", "Tıp Fakültesi", "Fizyoloji", "mentee"),
    ("Büşra", "Polat", "busra.polat@mail.com", "Edebiyat Öğrencisi", "Modern Şiir", "mentee"),
    ("Onur", "Koç", "onur.koc@mail.com", "Elektrik-Elektronik", "Devre Tasarımı", "mentee"),
    ("Naz", "Güneş", "naz.gunes@mail.com", "Endüstri Mühendisliği", "Optimizasyon", "mentee"),
    ("Emir", "Uçar", "emir.ucar@mail.com", "Biyomedikal", "Görüntüleme Sistemleri", "mentee"),
    ("Yasemin", "Er", "yasemin.er@mail.com", "Moleküler Biyoloji", "Genetik", "mentee"),
    ("Bora", "Şimşek", "bora.simsek@mail.com", "Matematik Öğrencisi", "Lineer Cebir", "mentee"),
    ("Selin", "Deniz", "selin.deniz@mail.com", "Çevre Mühendisliği", "Atık Yönetimi", "mentee"),
    ("Kaan", "Altun", "kaan.altun@mail.com", "Fizik", "Kuantum Mekaniği", "mentee"),
    ("Melis", "Türkmen", "melis.turkmen@mail.com", "Psikoloji", "Davranış Bilimleri", "mentee"),
    ("Tuna", "Gür", "tuna.gur@mail.com", "İstatistik", "Veri Görselleştirme", "mentee"),
    ("Eylül", "Avcı", "eylul.avci@mail.com", "Gıda Mühendisliği", "Beslenme", "mentee")
])

conn.commit()
conn.close()

print("models.py çalıştı!")

if os.path.exists("mentorship.db"):
    print("✅ mentorship.db başarıyla oluşturuldu!")
else:
    print("❌ mentorship.db dosyası oluşturulamadı!")
