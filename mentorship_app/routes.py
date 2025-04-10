from flask import Flask, jsonify, request, render_template
from database import get_db_connection

app = Flask(__name__)

# --------------------------------------------------------------------
# ANASAYFA ROTASI
# --------------------------------------------------------------------
@app.route("/")
def home_page():
    # index.html dosyasını render eder.
    return render_template("index.html")

# --------------------------------------------------------------------
# 1) Tüm Kullanıcıları Listele (JSON formatında)
# --------------------------------------------------------------------
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()

    users = []
    # Her kullanıcı için genişletilmiş alanları JSON olarak ekler.
    for row in rows:
        users.append({
            'id': row['id'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'occupation': row['occupation'],
            'skills': row['skills'],
            'role': row['role']
        })
    return jsonify(users)

# --------------------------------------------------------------------
# 2) Yeni Bir Kullanıcı Ekle (JSON body ile)
# --------------------------------------------------------------------
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json  # JSON formatında gelen veriler
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (first_name, last_name, email, occupation, skills, role) VALUES (?, ?, ?, ?, ?, ?)",
        (data['first_name'], data['last_name'], data['email'], data['occupation'], data['skills'], data['role'])
    )
    conn.commit()   # Değişiklikleri kaydeder
    conn.close()    # Bağlantıyı kapatır
    return jsonify({'message': 'User added successfully!'}), 201

# --------------------------------------------------------------------
# 3) Kullanıcıyı Güncelle (JSON body ile)
# --------------------------------------------------------------------
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json  # JSON formatında gelen güncelleme verileri
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET first_name=?, last_name=?, email=?, occupation=?, skills=?, role=? WHERE id=?",
        (data['first_name'], data['last_name'], data['email'], data['occupation'], data['skills'], data['role'], user_id)
    )
    conn.commit()   # Değişiklikleri kaydeder
    conn.close()    # Bağlantıyı kapatır
    return jsonify({'message': 'User updated successfully!'})

# --------------------------------------------------------------------
# 4) Kullanıcıyı Sil (JSON)
# --------------------------------------------------------------------
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User deleted successfully!'})

# --------------------------------------------------------------------
# 5) Kullanıcıları HTML'de Listeleme (Listelerken genişletilmiş alanları gösterir)
# --------------------------------------------------------------------
@app.route("/list-users", methods=["GET"])
def list_users_html():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()

    users = []
    for row in rows:
        users.append({
            'id': row['id'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'occupation': row['occupation'],
            'skills': row['skills'],
            'role': row['role']
        })
    # list_users.html şablonuna, kullanıcı listesini "users" olarak gönderir.
    return render_template("list_users.html", users=users)

# --------------------------------------------------------------------
# 6) HTML Formu Gösterme (GET) - Yeni Kullanıcı Ekleme Formunu gösterir
# --------------------------------------------------------------------
@app.route("/add-user-form", methods=["GET"])
def add_user_form():
    return render_template("add_user_form.html")

# --------------------------------------------------------------------
# 7) HTML Formunu İşleme (POST) - Kullanıcı ekleme formundan gelen verileri işler
# --------------------------------------------------------------------
@app.route("/submit-user", methods=["POST"])
def submit_user():
    print("Formdan gelen veriler:", request.form)  # Formdan gelen verileri konsola yazdırır.
    # Form verilerinden genişletilmiş alanları alır.
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    occupation = request.form.get("occupation")
    skills = request.form.get("skills")
    role = request.form.get("role")

    print(first_name, last_name, email, occupation, skills, role)  # Formdan gelen verileri konsola yazdırır.
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (first_name, last_name, email, occupation, skills, role) VALUES (?, ?, ?, ?, ?, ?)",
        (first_name, last_name, email, occupation, skills, role)
    )
    conn.commit()
    conn.close()

    return "Kullanıcı başarıyla eklendi! <a href='/list-users'>Listele</a>"

# --------------------------------------------------------------------
# 8) Kullanıcı Bilgilerini Düzenlemek için Formu Gösteren Rota (GET)
# --------------------------------------------------------------------
@app.route("/edit-user/<int:user_id>", methods=["GET"])
def edit_user_form(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return "Kullanıcı bulunamadı!", 404

    return render_template("edit_user.html", user=row)

# --------------------------------------------------------------------
# 9) Düzenleme Formundan Gelen Verileri İşleyen Rota (POST)
# --------------------------------------------------------------------
@app.route("/edit-user/<int:user_id>", methods=["POST"])
def edit_user_submit(user_id):
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    occupation = request.form.get("occupation")
    skills = request.form.get("skills")
    role = request.form.get("role")
    print(first_name, last_name, email, occupation, skills, role) 
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET first_name=?, last_name=?, email=?, occupation=?, skills=?, role=?
        WHERE id=?
    """, (first_name, last_name, email, occupation, skills, role, user_id))

    conn.commit()
    conn.close()

    return "Kullanıcı başarıyla güncellendi! <a href='/list-users'>Listeye dön</a>"

# --------------------------------------------------------------------
# Flask Uygulamasını Başlatma
# --------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
