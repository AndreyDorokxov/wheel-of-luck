from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = StringField('Введите почту', validators=[DataRequired()])
    password = PasswordField('Введите пароль', validators=[DataRequired()])
    password_2 = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Регистрация')


class LoginForm(FlaskForm):
    email = StringField('Введите почту', validators=[DataRequired()])
    password = PasswordField('Введите пароль', validators=[DataRequired()])
    submit = SubmitField('Вход')


class ProfileForm(FlaskForm):
    tokens = StringField('токен', validators=[DataRequired()])
    codeword1 = StringField('ключевое слово 1', validators=[DataRequired()])
    codeword2 = StringField('ключевое слово 2', validators=[DataRequired()])
    codeword3 = StringField('ключевое слово 3', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
