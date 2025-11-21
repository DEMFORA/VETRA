<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Kullanıcı Listesi</title>
</head>
<body>
    <h1>Kullanıcı Listesi</h1>
    <ul>
        {% for user in users %}
        <li>
            <strong>ID:</strong> {{ user.id }} |
            <strong>İsim:</strong> {{ user.name }} |
            <strong>Email:</strong> {{ user.email }} |
            <strong>Rol:</strong> {{ user.role }}
        </li>
        {% endfor %}
    </ul>

    <p><a href="/">Anasayfa</a></p>
</body>
</html>
