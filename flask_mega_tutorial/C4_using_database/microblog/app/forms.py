# в данном модуле, с помощью классов, прописываются вэб-формы (поля ввода) используемые в приложении

from flask_wtf import FlaskForm  # импорт базового встроенного класса вэб-формам
from wtforms import StringField, PasswordField, BooleanField, SubmitField  # импорт полей
from wtforms.validators import DataRequired  # импорт валидатора ввода значения

class LoginForm(FlaskForm):  # создание пользовательского класса из встроенного
    # далее создаются 4 класса - типы полей. Первый параметр каждого класса - описание (название) поля
    username = StringField('Username', validators=[DataRequired()])  # поле - имя пользователя, обязательное (DataRequired)
                                                                        # для заполнения поле, состоящее из строки
    password = PasswordField('Password', validators=[DataRequired()])  # поле - пароль, обязательное для заполнения
    remember_me = BooleanField('Remember me')  # поле - запомнить меня, не обязательное, с булевым значением
    submit = SubmitField('Sign in')  # чекбокс, не обязательный
