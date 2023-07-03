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

from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('main_page.html')


@app.route('/pow/', methods=['GET', 'POST'])
def square():
    if request.method == 'POST':
        number = int(request.form.get('number'))
        return f"Число {number} в квадрате: {number * number}"
    return render_template('number_pow.html')


@app.route('/email/', methods=['GET', 'POST'])
def get_email():
    if request.method == 'POST':
        username = request.form.get('username')
        user_email = request.form.get('email')
        response = make_response(redirect(url_for('greetings', name=username)))
        response.set_cookie('name', username)
        return response
    return render_template('email_form.html')


@app.route('/greetings/<name>')
def greetings(name):
    return render_template('greetings.html', name=name)


@app.route('/greetings')
def user_quit():
    response = make_response(redirect('/email/'))
    response.delete_cookie('name')
    return response


if __name__ == '__main__':
    app.run()
