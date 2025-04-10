from flask import Flask

app = Flask(__name__)  # Flask uygulamasını başlat

@app.route("/")  # Ana sayfa için route
def home():
    return "VETRA Uygulmasına Hoş Geldiniz!"  # Basit bir çıktı

if __name__ == "__main__":
    print("🚀 VETRA uygulaması başlatılıyor...")
    app.run(debug=True, use_reloader=True)  # Flask sunucusunu çalıştır ve otomatik yeniden yüklemeyi etkinleştir
