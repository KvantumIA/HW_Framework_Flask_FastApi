from flask import Flask, request, render_template, redirect, flash, url_for
from flask_wtf.csrf import CSRFProtect
import secrets
from task_4_form import RegistrationForm
from task_4_models import RegistrationUser, db
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex()
csrf = CSRFProtect(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../instance/task_4_db.database'

db.init_app(app)


@app.cli.command("init-database")
def init_db():
    db.create_all()
    print('OK')


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/data/')
def data():
    return 'Your data!'


# @app.route('/login/', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if request.method == 'POST' and form.validate():
#         pass
#     return render_template('login.html', form=form)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        # Обработка данных из формы
        username = form.username.data
        firstname = form.firstname.data
        email = form.email.data
        birthday = form.birthday.data
        password = form.password.data
        personal_data = form.personal_data.data
        fill_registration_user_db(username, firstname, email, password, birthday, personal_data)
    return render_template('register.html', form=form)


def fill_registration_user_db(username, firstname, email, password, birthday, personal_data):
    secret_password = hash_password(password)
    if test_unique_user(username, email):
        user = RegistrationUser(username=username,
                                firstname=firstname,
                                email=email,
                                password=secret_password,
                                birthday=birthday,
                                personal_data=personal_data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно!', 'success')
        return redirect(url_for('register'))
    flash('Пользователь уже зарегистрирован!', 'alert')
    return redirect(url_for('register'))


def test_unique_user(username, email):
    user_name = RegistrationUser.query.filter_by(username=username).first() is not None
    user_email = RegistrationUser.query.filter_by(email=email).first() is not None
    return not (user_name or user_email)


def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


if __name__ == '__main__':
    app.run(debug=True)
