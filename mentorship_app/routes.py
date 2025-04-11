from flask import Flask, jsonify, request, render_template
from database import get_db_connection

app = Flask(__name__)

# --------------------------------------------------------------------
# ANASAYFA
# --------------------------------------------------------------------
@app.route("/")
def home_page():
    return render_template("index.html")

# --------------------------------------------------------------------
# TÜM KULLANICILARI LİSTELE (JSON)
# --------------------------------------------------------------------
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()

    users = [
        {
            'id': row['id'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'occupation': row['occupation'],
            'skills': row['skills'],
            'role': row['role']
        } for row in rows
    ]
    return jsonify(users)

# --------------------------------------------------------------------
# YENİ KULLANICI EKLE (JSON)
# --------------------------------------------------------------------
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (first_name, last_name, email, occupation, skills, role) VALUES (?, ?, ?, ?, ?, ?)",
        (data['first_name'], data['last_name'], data['email'], data['occupation'], data['skills'], data['role'])
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'User added successfully!'}), 201

# --------------------------------------------------------------------
# KULLANICI GÜNCELLE (JSON)
# --------------------------------------------------------------------
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET first_name=?, last_name=?, email=?, occupation=?, skills=?, role=? WHERE id=?",
        (data['first_name'], data['last_name'], data['email'], data['occupation'], data['skills'], data['role'], user_id)
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'User updated successfully!'})

# --------------------------------------------------------------------
# KULLANICI SİL (JSON)
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
# TÜM KULLANICILARI HTML'DE GÖSTER
# --------------------------------------------------------------------
@app.route("/list-users", methods=["GET"])
def list_users_html():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()

    users = [
        {
            'id': row['id'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'occupation': row['occupation'],
            'skills': row['skills'],
            'role': row['role']
        } for row in rows
    ]
    return render_template("list_users.html", users=users)

# --------------------------------------------------------------------
# KULLANICI EKLEME FORMU (HTML)
# --------------------------------------------------------------------
@app.route("/add-user-form", methods=["GET"])
def add_user_form():
    return render_template("add_user_form.html")

@app.route("/submit-user", methods=["POST"])
def submit_user():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    occupation = request.form.get("occupation")
    skills = request.form.get("skills")
    role = request.form.get("role")

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
# KULLANICI DÜZENLEME FORMU (HTML)
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

@app.route("/edit-user/<int:user_id>", methods=["POST"])
def edit_user_submit(user_id):
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    occupation = request.form.get("occupation")
    skills = request.form.get("skills")
    role = request.form.get("role")

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
# MENTÖR-MENTEE EŞLEŞME ROTASI
# --------------------------------------------------------------------
@app.route("/match-users", methods=["GET"])
def match_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE role='mentor'")
    mentors = cursor.fetchall()

    cursor.execute("SELECT * FROM users WHERE role='mentee'")
    mentees = cursor.fetchall()
    conn.close()

    matches = []

    for mentee in mentees:
        mentee_skills = set(map(str.strip, mentee['skills'].lower().split(',')))
        mentor_scores = []

        for mentor in mentors:
            mentor_skills = set(map(str.strip, mentor['skills'].lower().split(',')))
            score = len(mentee_skills & mentor_skills)

            if score > 0:
                mentor_scores.append({
                    'mentor': mentor,
                    'score': score
                })

        # Puanı 0'dan büyük olanları sırala ve ilk 3'ü al
        mentor_scores.sort(key=lambda x: x['score'], reverse=True)
        top_matches = mentor_scores[:3]

        matches.append({
            'mentee': mentee,
            'mentors': top_matches
        })


    # 🎯 Return ifadesi dışarıda olmalı
    return render_template("match_results.html", matches=matches)

        
# --------------------------------------------------------------------
# UYGULAMA BAŞLATMA
# --------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
