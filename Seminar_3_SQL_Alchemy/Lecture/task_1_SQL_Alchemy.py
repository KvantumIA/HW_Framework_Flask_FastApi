from flask import Flask
from Seminar_3_SQL_Alchemy.Lecture.models import db, User, Post, Comment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.database'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@hostname/db_name'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://username:password@hostname/db_name'

db.init_app(app)


@app.route('/')
def index():
    return 'Hi!'


@app.cli.command("init-database")
def init_db():
    db.create_all()
    print('OK')


@app.cli.command("add-john")
def add_user():
    user = User(username='John', email='john@example.com')
    db.session.add(user)
    db.session.commit()
    print('John add in DB!')


@app.cli.command("edit-john")
def edit_user():
    user = User.query.filter_by(username='John').first()
    user.email = 'new_email@example.com'
    db.session.commit()
    print('Edit John mail in DB!')


@app.cli.command("del-john")
def del_user():
    user = User.query.filter_by(username='John').first()
    db.session.delete(user)
    db.session.commit()
    print('Delete John from DB!')


if __name__ == '__main__':
    app.run(debug=True)
