from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    age = db.Column(db.String(120), nullable=True)
    sex = db.Column(db.String(60), nullable=True)
    group = db.Column(db.Integer, nullable=True)
    id_faculty = db.Column(db.Integer, db.ForeignKey('faculty.id'))

    def __repr__(self):
        return f'Student({self.first_name}, {self.last_name}, {self.age}, {self.sex}, {self.group})'


class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=True)
    students = db.relationship('Students', backref='faculty', lazy=True)

    def __repr__(self):
        return f'Faculty({self.name})'
