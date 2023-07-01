from pathlib import PurePath, Path

from flask import Flask, render_template, url_for, request, abort, flash, redirect
from werkzeug.utils import secure_filename

# Задание 7
#
# Создать страницу, на которой будет форма для ввода числа и кнопка "Отправить".
# При нажатии на кнопку будет произведено перенаправление на страницу с результатом,
# где будет выведено введенное число и его квадрат.
#
# Задание 9
#
# Создать страницу, на которой будет форма для ввода имени и электронной почты,
# при отправке которой будет создан cookie-файл с данными пользователя,
# а также будет произведено перенаправление на страницу приветствия,
# где будет отображаться имя пользователя.
# На странице приветствия должна быть кнопка «Выйти»,
# при нажатии на которую будет удалён cookie-файл с данными пользователя
# и произведено перенаправление на страницу ввода имени и электронной почты.


app = Flask(__name__)


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/greetings', methods=['GET', 'POST'])
def hello():
    app.secret_key = b"4353444adfa"
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        flash(f'Hello, {user_name}!', 'success')
        return redirect(url_for('hello'))
    return render_template('name_form.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        file_name = secure_filename(file.filename)
        file.save(PurePath.joinpath(Path.cwd(), 'uploads', file_name))
        return f'{file_name} uploaded'
    return render_template('upload_img.html')


users = {
    'user1': 'password1',
    'user2': 'password2'
}


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_login = request.form.get('user_login')
        password = request.form.get('password')
        if user_login not in users:
            return f'User {user_login} not found.'
        if users.get(user_login) == password:
            return f'Hello, {user_login}'
        else:
            return f'Password incorrect.'
    return render_template('login_form.html')


@app.route('/text', methods=['GET', 'POST'])
def compute_words():
    if request.method == 'POST':
        text = request.form.get('text')
        res = len(text.split())
        return f"Количество слов: {res}"
    return render_template('text_input.html')


@app.route('/calc', methods=['GET', 'POST'])
def calculate():
    if request.method == 'POST':
        num1 = int(request.form.get('num1'))
        num2 = int(request.form.get('num2'))
        oper = request.form.get('operation')
        if oper == 'add':
            return f'{num1} + {num2} = {num1 + num2}'
        if oper == 'subtract':
            return f'{num1} - {num2} = {num1 - num2}'
        if oper == 'multiply':
            return f'{num1} * {num2} = {num1 * num2}'
        if oper == 'divide':
            return f'{num1} / {num2} = {num1 / num2}'
        return f"Произошла непредвиденная ошибка."
    return render_template('calc.html')


@app.route('/age/', methods=['GET', 'POST'])
def user_age():
    if request.method == 'POST':
        username = request.form.get('username')
        age = int(request.form.get('age'))
        if age <= 0:
            abort(403)
        return f"Возраст пользователя {username}: {age}"
    return render_template('user_age.html')


@app.errorhandler(403)
def error403(e):
    return render_template('error403.html'), 403


if __name__ == '__main__':
    app.run()
