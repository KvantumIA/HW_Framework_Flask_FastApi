from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    group = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(120), nullable=True)
    ranked = db.relationship('Ranked', backref='student', lazy=True)

    def __repr__(self):
        return f'Student({self.first_name}, {self.last_name}, {self.email}, {self.group})'


class Ranked(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_student = db.Column(db.Integer, db.ForeignKey('students.id'))
    name = db.Column(db.String(120), nullable=True)
    rank = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'Ranked({self.id_student}, {self.name}, {self.rank})'
