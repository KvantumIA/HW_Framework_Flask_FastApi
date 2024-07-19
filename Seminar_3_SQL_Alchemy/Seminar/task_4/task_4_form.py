from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError


def validate_password(form, field):
    import re
    password = field.data
    if len(password) < 8:
        raise ValidationError('Пароль должен содержать не менее 8 символов.')
    if not re.search(r'[A-Za-z]', password):
        raise ValidationError('Пароль должен содержать хотя бы одну букву.')
    if not re.search(r'\d', password):
        raise ValidationError('Пароль должен содержать хотя бы одну цифру.')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    firstname = StringField('First name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    birthday = DateField('Birthday', format='%Y-%m-%d')
    password = PasswordField('Password', validators=[DataRequired(), validate_password])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    personal_data = SelectField('согласие на обработку персональных данных', choices=[('yes', 'Да'), ('no', 'Нет')])


