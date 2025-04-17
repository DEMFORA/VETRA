from flask import Flask, jsonify, request, render_template
import sqlite3
from database import get_db_connection

app = Flask(__name__)

PROFESSION_TOPICS = {
    "Yazılım Mühendisi": ["Python", "java", "c++", "javascript", "flask","veri analizi"],
    "Tıp Doktoru": ["anatomi", "fizyoloji", "kardiyoloji", "biyoloji"],
    "Mimar": ["autocad", "tasarım", "sketchup"],
    "Makine Mühendisi": ["solidworks", "termodinamik", "cad", "cam"],
    "Edebiyatçı": ["şiir", "roman", "yaratıcı yazarlık", "edebiyat", "editörlük"]
}

@app.route("/")
def home_page():
    return render_template("index.html")

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

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User deleted successfully!'})

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

@app.route("/add-user-form", methods=["GET"])
def add_user_form():
    return render_template("add_user_form.html")

# ✅ GÜNCELLENEN BÖLÜM BURASI:
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

    # Eski sade metin yerine tasarımlı HTML sayfası dönüyoruz
    return render_template("user_added.html", first_name=first_name)

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

@app.route("/match-users", methods=["GET"])
def match_users():
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE role='mentor'")
    mentors = cursor.fetchall()

    cursor.execute("SELECT * FROM users WHERE role='mentee'")
    mentees = cursor.fetchall()

    expertise_score = 3
    profession_score = 1
    match_results = []

    for mentee in mentees:
        mentee_interests = set(map(str.strip, mentee['skills'].lower().split(',')))
        mentor_scores = []

        for mentor in mentors:
            score = 0
            mentor_skills = set(map(str.strip, mentor['skills'].lower().split(',')))
            mentor_profession_topics = set(map(str.lower, PROFESSION_TOPICS.get(mentor['occupation'], [])))

            for interest in mentee_interests:
                if interest in mentor_skills:
                    score += expertise_score
            if mentee_interests & mentor_profession_topics:
                score += profession_score

            if score > 0:
                mentor_scores.append({
                    'mentor': mentor,
                    'score': score
                })

        mentor_scores.sort(key=lambda x: x['score'], reverse=True)
        top_matches = mentor_scores[:3]

        selected_mentor = None
        if mentee['selectedMentId']:
            selected_mentor = next((m for m in mentors if m['id'] == mentee['selectedMentId']), None)

        match_results.append({
            'mentee': mentee,
            'mentors': top_matches,
            'selectedMentId': mentee['selectedMentId'],
            'selected_mentor': selected_mentor
        })

    conn.close()
    return render_template("match_results.html", matches=match_results)

@app.route("/assign-mentor", methods=["POST"])
def assign_mentor():
    data = request.json
    mentee_id = data.get("mentee_id")
    mentor_id = data.get("mentor_id")

    if not mentee_id or not mentor_id:
        return jsonify({"error": "Eksik veri gönderildi."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE users SET selectedMentId = ? WHERE id = ? AND role = 'mentee'", (mentor_id, mentee_id))
        conn.commit()
        return jsonify({"message": "Mentör başarıyla atandı!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route("/remove-mentor", methods=["POST"])
def remove_mentor():
    data = request.json
    mentee_id = data.get("mentee_id")

    if not mentee_id:
        return jsonify({"error": "Mentee ID eksik"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE users SET selectedMentId = NULL WHERE id = ? AND role = 'mentee'", (mentee_id,))
        conn.commit()
        return jsonify({"message": "Mentör kaldırıldı."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
