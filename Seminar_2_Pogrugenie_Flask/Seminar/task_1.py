from flask import Flask, url_for, render_template, request, flash, redirect, make_response, session, abort
from markupsafe import escape
from pathlib import PurePath, Path
from werkzeug.utils import secure_filename
import secrets
import logging

secrets.token_hex()


app = Flask(__name__)
logger = logging.getLogger(__name__)
app.secret_key = 'ce35fd2542fd202d27bbc270155fe3402652807512126f88879857039d93182a'

CONTEXT = {}
TASK_INFO = {'task_1': 'Создать страницу, на которой будет кнопка "Нажми меня"'
                       ', при нажатии на которую будет переход на другую '
                       'страницу с приветствием пользователя по имени.',
             'task_2': 'Создать страницу, на которой будет изображение и '
                       'ссылка на другую страницу, на которой будет '
                       'отображаться форма для загрузки изображений.',
             'task_3': 'Создать страницу, на которой будет форма для ввода '
                      'логина и пароля При нажатии на кнопку "Отправить" будет'
                      ' произведена проверка соответствия логина и пароля и '
                      'переход на страницу приветствия пользователя или'
                      ' страницу с ошибкой.',
             'task_4': 'Создать страницу, на которой будет форма для ввода '
                      'текста и кнопка "Отправить". При нажатии кнопки будет '
                      'произведен подсчет количества слов в тексте и переход '
                      'на страницу с результатом.',
             'task_5': 'Создать страницу, на которой будет форма для ввода '
                       'двух чисел и выбор операции (сложение, вычитание, '
                       'умножение или деление) и кнопка "Вычислить" При '
                       'нажатии на кнопку будет произведено вычисление '
                       'результата выбранной операции и переход на страницу с '
                       'результатом.',
             'task_6': 'Создать страницу, на которой будет форма для ввода '
                       'имени и возраста пользователя и кнопка "Отправить" При'
                       ' нажатии на кнопку будет произведена проверка возраста'
                       ' и переход на страницу с результатом или на страницу с'
                       ' ошибкой в случае некорректного возраста.',
             'task_7': 'Создать страницу, на которой будет форма для ввода '
                       'числа и кнопка "Отправить" При нажатии на кнопку будет'
                       ' произведено перенаправление на страницу с результатом'
                       ', где будет выведено введенное число и его квадрат.',
             'task_8': 'Создать страницу, на которой будет форма для ввода '
                       'имени и кнопка "Отправить" При нажатии на кнопку будет'
                       ' произведено перенаправление на страницу с flash '
                       'сообщением, где будет выведено "Привет, {имя}!".',
             'task_9': 'Создать страницу, на которой будет форма для ввода '
                       'имени и электронной почты При отправке которой будет '
                       'создан cookie файл с данными пользователя Также будет '
                       'произведено перенаправление на страницу приветствия, '
                       'где будет отображаться имя пользователя. На странице '
                       'приветствия должна быть кнопка "Выйти" При нажатии на '
                       'кнопку будет удален cookie файл с данными пользователя'
                       ' и произведено перенаправление на страницу ввода имени'
                       ' и электронной почты.'}

account = {'login': 'Ivan', 'password': '1234'}


@app.route('/')
def base():
    return redirect('main')


@app.route('/main/')
def main():
    global CONTEXT
    CONTEXT = {'title': 'Задача', 'name': 'Иван', 'img_url_name': 'Котик'}
    img_url = url_for('static', filename='img/img_1.jpg')
    return render_template('main.html', **CONTEXT, img_url=img_url, **TASK_INFO)

# -------------------------------------------------------------


# Задание №1
@app.route('/task1/')
def task1():
    return render_template('task1.html', **CONTEXT)

# -------------------------------------------------------------


# Задание №2
@app.route('/task2/', methods=['GET', 'POST'])
def task2():
    if request.method == 'POST':
        file = request.files.get('file')
        file_name = secure_filename(file.filename)
        file.save(PurePath.joinpath(Path.cwd(), 'uploads', file_name))
        return f"Файл {file_name} загружен на сервер"
    return render_template('task2.html', **CONTEXT)

# -------------------------------------------------------------


# Задание №3
@app.route('/authorization/', methods=['GET', 'POST'])
def task3():
    if request.method == 'POST':
        auth_login = request.form.get('auth_login')
        auth_password = request.form.get('auth_password')
        if auth_login == account.get('login') and auth_password == account.get('password'):
            return f'{auth_login}, авторизация успешна!'
        else:
            return f'Пользователя, {auth_login}, не существует. Повторите авторизацию.'
    return render_template('task3.html', **CONTEXT)

# -------------------------------------------------------------


# Задание №4
@app.route('/text/', methods=['GET', 'POST'])
def task4():
    if request.method == 'POST':
        text = request.form.get('text')
        return f'Количество слов - {len(text.split())}'
    return render_template('task4.html', **CONTEXT)

# -------------------------------------------------------------


# Задание №5
@app.route('/sum/', methods=['GET', 'POST'])
def task5():
    if request.method == 'POST':
        num1 = int(request.form.get('num1'))
        num2 = int(request.form.get('num2'))
        sign = request.form.get('options')
        if sign == 'option1':
            return f'Сумма чисел равна - {num1 + num2}'
        elif sign == 'option2':
            return f'Сумма чисел равна - {num1 - num2}'
        elif sign == 'option3':
            return f'Сумма чисел равна - {num1 * num2}'
        elif sign == 'option4':
            if num2 == 0:
                return 'Ошибка! Делить на 0 нельзя!'
            return f'Сумма чисел равна - {num1 / num2}'
        else:
            return f'Ошибка {sign}'
    return render_template('task5.html', **CONTEXT)

# -------------------------------------------------------------


# Задание №6
@app.route('/age/', methods=['GET', 'POST'])
def task6():
    if request.method == 'POST':
        age = request.form.get('age')
        name = request.form.get('name')
        if age >= '18':
            return f'{name}, Вы допущены до контента'
        abort(403)
    return render_template('task6.html', **CONTEXT)


@app.errorhandler(403)
def page_not_found(e):
    logger.warning(e)
    context = {'title': 'Ошибка', 'text': 'Ваш возраст меньше 18 лет!'}
    return render_template('403.html', **context), 403

# -------------------------------------------------------------


# Задание №7
@app.route('/square/', methods=['GET', 'POST'])
def task7():
    if request.method == 'POST':
        num = int(request.form.get('num'))
        return redirect(url_for('task7_square', num=num))
    return render_template('task7.html', **CONTEXT)


@app.route('/num_square/<num>')
def task7_square(num):
    return f'Квадрат числа {num}, равняется - {int(num) ** 2}'

# -------------------------------------------------------------


# Задание №8
@app.route('/name/', methods=['GET', 'POST'])
def task8():
    if request.method == 'POST':
        name = request.form.get('name')
        flash(f'Привет, {name}', 'success')
        return redirect(url_for('task8'))
    return render_template('task8.html', **CONTEXT)

# -------------------------------------------------------------


# Задание №9
@app.route('/getcookie/', methods=['GET', 'POST'])
def task9():
    if request.method == 'POST':
        session['name_cookie'] = request.form.get('username')
        session['email_cookie'] = request.form.get('email')
        return redirect(url_for('task9_answer'))
    return render_template('task9.html', **CONTEXT)


@app.route('/task9_answer/')
def task9_answer():
    if 'name_cookie' in session:
        return render_template('task9_answer.html', my_name=session['name_cookie'], **CONTEXT)


@app.route('/logout/')
def logout():
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('task9'))


if __name__ == '__main__':
    app.run(debug=True)
