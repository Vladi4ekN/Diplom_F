from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

users = {'user1': '1111', 'user2': '2222'}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('bookstore'))  # Перенаправление на новую страницу
        else:
            flash('Неверное имя пользователя или пароль')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/bookstore')
@login_required
def bookstore():
    html_template = '''
    <!doctype html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bookstore Links</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 50px;
                background-color: #EED5B7;
            }
            .button {
                display: inline-block;
                padding: 10px 20px;
                margin: 10px;
                background-color: #8B7D6B;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }
            .button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <h1>Добро пожаловать, любители книг!</h1>
        <h2>Ниже, вы сможете выбрать популярные сайты и выбрать книгу по душе!</h2>
        <p>Приятного чтения!</p>
        <a href="https://www.bookvoed.ru/?ysclid=m2utrlv32g363030526" class="button">Буквоед</a>
        <a href="https://dk-spb.ru/?ysclid=m2utsvbbr317777375" class="button">Дом книг</a>
        <a href="https://www.chitai-gorod.ru/?ysclid=m2uttt1zka590744434" class="button">Читай-город</a>
        <br><br>
        <a href="/logout" class="button">Выйти</a>
    </body>
    </html>
    '''
    return html_template

@app.route('/protected')
@login_required
def protected():
    return 'Вы вошли в защищенную зону!'

if __name__ == '__main__':  # Исправлено на __name__
    app.run(debug=True)
