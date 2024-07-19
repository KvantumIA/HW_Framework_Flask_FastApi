from flask_sqlalchemy import SQLAlchemy

db_library = SQLAlchemy()


class Book(db_library.Model):
    id = db_library.Column(db_library.Integer, primary_key=True)
    name = db_library.Column(db_library.String(80), nullable=True)
    age_create = db_library.Column(db_library.String(60), nullable=True)
    count = db_library.Column(db_library.String(60), nullable=True)
    id_author = db_library.Column(db_library.Integer, db_library.ForeignKey('author.id'))
    # authors = db_library.relationship('Author', secondary='book_author', backref='books', lazy=True)

    def __repr__(self):
        return f'Book({self.name}, {self.age}, {self.count}, {self.id_author})'


class Author(db_library.Model):
    id = db_library.Column(db_library.Integer, primary_key=True)
    first_name = db_library.Column(db_library.String(80), nullable=True)
    last_name = db_library.Column(db_library.String(80), nullable=True)
    books = db_library.relationship('Book', backref='author', lazy=True)

    def __repr__(self):
        return f'Author({self.first_name}, {self.last_name})'


# class BookAuthor(db_library.Model):
#     id = db_library.Column(db_library.Integer, primary_key=True)
#     book_id = db_library.Column(db_library.Integer, db_library.ForeignKey('book.id'))
#     author_id = db_library.Column(db_library.Integer, db_library.ForeignKey('author.id'))