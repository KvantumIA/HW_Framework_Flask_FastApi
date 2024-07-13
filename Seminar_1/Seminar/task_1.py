from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


# @app.route('/about/')
# def about():
#     return 'About!'
#
#
# @app.route('/contact/')
# def contact():
#     return 'Contact'


@app.route('/<int:num_1>/<int:num_2>/')
def sum_num(num_1: int, num_2: int) -> str:
    return str(num_1 + num_2)


@app.route('/String/<string:text>/')
def len_str(text: str) -> str:
    return str(len(text))


@app.route('/index/')
def first_page():
    return render_template('index.html')


@app.route('/student/')
def second_page():
    head = {'first_name': 'Имя',
            'second_name': 'Фамилия',
            'birthday': 'Дата рождения',
            'average_score': 'Средний бал'}
    student = [{'first_name': 'Ivan',
                'second_name': 'Ivanov',
                'birthday': '01.01.1990',
                'average_score': 12},
               {'first_name': 'Petr',
                'second_name': 'Petrov',
                'birthday': '02.02.1991',
                'average_score': 8}]
    context = {'students': student}
    return render_template('index.html', **head, **context)


@app.route('/news/')
def news_page():
    news_ = [{'title': 'Новые новости', 'content': 'самые свежие новости',
              'date': '01.01.2024'},
             {'title': 'Старые новости', 'content': 'старые новости',
              'date': '01.01.2023'},
             {'title': 'Новости спорта', 'content': 'Футбольный матч',
              'date': '03.06.2024'}]
    context = {'news': news_}
    return render_template('index_2.html', **context)


@app.route('/main/')
def base_page():
    context = {'title': 'Главная'}
    return render_template('main.html', **context)


@app.route('/about/')
def team_page():
    context = {'title': 'О нас'}
    return render_template('about.html', **context)


@app.route('/contact/')
def contact_page():
    context = {'title': 'Контакты'}
    return render_template('contact.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
