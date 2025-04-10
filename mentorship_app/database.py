import sqlite3

def get_db_connection():
    # mentorship.db dosyasıyla bağlantı kurar.
    # check_same_thread=False: Aynı thread dışındaki erişimlere izin verir.
    # timeout=10: Kilitlenme durumunda 10 saniyeye kadar bekler.
    conn = sqlite3.connect('mentorship.db', check_same_thread=False, timeout=10)
    # Sorgu sonuçlarını sözlük (dict) olarak kullanabilmek için row_factory ayarlanır.
    conn.row_factory = sqlite3.Row
    # Eğer veritabanı kilitlenmişse, 5000 milisaniye (5 saniye) beklemeyi sağlayan busy_timeout ayarı.
    conn.execute("PRAGMA busy_timeout = 5000")
    return conn
