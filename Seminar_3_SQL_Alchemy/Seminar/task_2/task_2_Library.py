from flask import Flask, render_template
from Seminar_3_SQL_Alchemy.Seminar.task_2.models_library import db_library, Author, Book
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../instance/library_db.db'

db_library.init_app(app)


@app.cli.command("init-db-library")
def init_db():
    db_library.create_all()
    print('OK')


@app.cli.command("fill-db-library")
def fill_tables():
    count = 5
    # Добавляем Авторов
    for user in range(1, count + 1):
        new_user = Author(first_name=f'Author_name {user}', last_name=f'Author {user}')
        db_library.session.add(new_user)
    db_library.session.commit()
    # Добавляем книги
    for book in range(1, count ** 2):
        author = Author.query.filter_by(first_name=f'Author_name {book % count + 1}').first()
        new_book = Book(name=f'Book name {book}',
                        age_create=random.randint(1980, 2024),
                        count=random.randint(1, 20),
                        author=author)
        db_library.session.add(new_book)
    db_library.session.commit()


@app.route('/')
def index():
    return render_template('library.html')


@app.route('/library/')
def library():
    libraries = Book.query.all()
    context = {'library': libraries, 'title': 'Библиотека'}
    return render_template('library.html', **context)


@app.route('/authors/')
def authors():
    author = Author.query.all()
    context = {'author': author, 'title': 'Библиотека'}
    return render_template('authors.html', **context)


@app.route('/library-search/', methods=['GET', 'POST'])
def library_search():
    search_ = 'Book name 2'
    search = Book.query.filter_by(name=search_).all()
    context = {'search': search, 'title': 'Поиск'}
    return render_template('library_search.html', **context)


@app.route('/library-search-author/', methods=['GET', 'POST'])
def library_search_author():
    search_ = 'Author_name 2'
    search = Author.query.filter_by(first_name=search_)
    libraries = Book.query.all()
    context = {'author': search, 'library': libraries, 'title': 'Поиск'}
    return render_template('authors.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
