from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/main/')
def base_page():
    context = {'title': 'Главная'}
    return render_template('main.html', **context)


@app.route('/clothes/')
def clothes_page():
    head = {'title': 'Одежда'}
    product = [{'name': 'Футболка',
                'price': 1000,
                'description': 'Удобная и стильная футболка.',
                'images': '../static/img/T-shirt.png'},
               {'name': 'Джинсы',
                'price': 2000,
                'description': 'Классические джинсы, подходящие для любого случая.',
                'images': '../static/img/jeans.jpeg'},
               {'name': 'Шорты',
                'price': 1200,
                'description': 'Удобные шорты для летней погоды.',
                'images': '../static/img/shirt.jpeg'}
               ]
    context = {'product': product}
    return render_template('clothes.html', **head, **context)


@app.route('/shoes/')
def shoes_page():
    context = {'title': 'Обувь'}
    return render_template('shoes.html', **context)


@app.route('/jackets/')
def jackets_page():
    context = {'title': 'Куртки'}
    return render_template('jackets.html', **context)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.2', port=8080)
