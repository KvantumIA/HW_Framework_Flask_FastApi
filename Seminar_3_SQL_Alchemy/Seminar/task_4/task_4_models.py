from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class RegistrationUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=True)
    firstname = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    birthday = db.Column(db.String(80), nullable=True)
    password = db.Column(db.String(80), nullable=True)
    personal_data = db.Column(db.String(60), nullable=True)

    def __repr__(self):
        return f'User({self.username}, {self.email})'
