# в данном модуле, с помощью классов, прописываются вэб-формы (поля ввода) для входа пользователя в систему и для регистрации
# нового пользователя, используемые в приложении и их логика. Созданные здесь формы имеют соответствующие шаблоны в папке
# с шаблонами, и эти шаблоны позволяют отображать формы

from flask_wtf import FlaskForm  # импорт базового встроенного класса вэб-формам
from wtforms import StringField, PasswordField, BooleanField, SubmitField  # импорт встроенных полей
from wtforms import TextAreaField  # многострочное поле
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length  # импорт валидаторов ввода значений в поля
                            # для регистрации. Length - валидатор длинны строки
import sqlalchemy as sa  # для работы с БД (запросы, функции и т.д.)
from flask_mega_tutorial.C7_error_handling.microblog.app import db  # импорт БД
from flask_mega_tutorial.C7_error_handling.microblog.app.models import User  # импорт модели таблицы Пользователи


class LoginForm(FlaskForm):  # создание пользовательского класса из встроенного
    """
    Данный класс является кастомным, дочерним от встроенного FlaskForm. Представляет из себя форму для входа пользователя
     в систему. Имеет 4 атрибута, из 3 поля (2 обязательных для заполнения) для заполнения и один чекбокс. Прорисовка
     этой формы выполнена в шаблоне login.html
    """
    # далее создаются 4 класса - типы полей. Первый параметр каждого класса - описание (название) поля
    username = StringField('Username', validators=[DataRequired()])  # поле - имя пользователя, обязательное (DataRequired)
                                                                        # для заполнения поле, состоящее из строки
    password = PasswordField('Password', validators=[DataRequired()])  # поле - пароль, обязательное для заполнения
    remember_me = BooleanField('Remember me')  # поле - запомнить меня, не обязательное, с булевым значением
    submit = SubmitField('Sign in')  # чекбокс, не обязательный


class RegistrationForm(FlaskForm):
    """
    Данный класс кастомный, имеет 5 атрибутов и два метода, является дочерним от встроенного в библиотеку flask_wtf
    класса FlaskForm создает регистрационную форму, состоящую из нескольких полей. Каждое поле в виде атрибута класса.
    Обеспечивается проверка (валидация) типа вводимых данных. Имеет два метода, каждый из них соответственно проверяет
    свободны ли введенные пользователем имя и имейл. Для отображения этой формы в папке с шаблонами нужно реализовать
    соответствующий шаблон
    """
    username = StringField('Username', validators=[DataRequired()])  # поле для регистрации имени пользователя.
                                    # Username - заголовок, validators=[DataRequired()] - влидация чтобы поле не было пустым

    email = StringField('Email', validators=[DataRequired(), Email()])  # поле для регистрации имейла. Email() -
                                    # специальный валидатор для имейла. !!! требует доп установки: pip install email-validator

    password = PasswordField('Password', validators=[DataRequired()])  # поле для регистрации пароля. С заголовком
                                    # и одним валидатором

    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])  # поле подтверждения пароля. Заголовок
                                    # и два валидатора. EqualTo - валидатор сравнивает значения двух полей

    submit = SubmitField('Register')  # кнопка отправки формы для регистрации с надписью "Register"

    # !!! ВАЖНО !!! Далее я создаю два пользовательских валидатора. Валидаторы создаваемые по шаблону validate_<название_поля>
    # WTForms использует их в качестве пользовательских валидаторов и вызывает их в дополнение к стандартным валидаторам.
    def validate_username(self, username):
        """
        Этот метод проверяет существует ли в БД пользователь с таким именен, если существует, вызывает исключение с
        соответствующим сообщением
        :param username: имя пользователя введенное в поле для регистрации
        :return:
        """
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username!')

    def validate_email(self, email):
        """
        Этот метод проверяет существует ли в БД пользователь с таким имейлом, если существует, вызывает исключение с
        соответствующим сообщением
        :param email: имейл пользователя введенный в поле для регистрации
        :return:
        """
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address!')


class EditProfileForm(FlaskForm):
    """
    Это класс редактора профиля пользователя (форма). Состоит из нескольких полей для заполнения. Задача этого класса -
    создать форму для редактирования профиля с «умной» проверкой уникальности имени. Главная проблема, которую он решает:
    как не выдавать ошибку «это имя уже занято», когда пользователь сохраняет свое же текущее имя.
    """
    username = StringField('Username', validators=[DataRequired()])  # настройка поля "имя пользователя"
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])  # настройка поля "о себе".
                                # TextAreaField - многострочное поле. Валидатор Length - проверяет соблюдение заданной
                                # длинны строки (измерение в символах)
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        """
        original_username - это имя пользователя получаемое от встроенного класса current_user (содержит имя текущего
        пользователя), эта передача происходит при создании формы в функции просмотра edit_profile в файле routes.py.
        Аргумент original_username прописывается отдельно перед неименованными и именованными аргументами, поскольку он
        далее прописывается как переменная экземпляра
        :param original_username: текущее имя пользователя
        :param args: любые неименованные аргументы
        :param kwargs: именованные аргументы
        """
        super().__init__(*args, **kwargs)
        self.original_username = original_username  # создается переменная экземпляра в которой сохраняется текущее имя
                                                # пользователя, т.е. имя пользователя на момент входа на страницу
                                                # редактирования профиля, дальше в методе validate_username, это имя будет
                                                # сравниваться с именем в поле "username" формы

    def validate_username(self, username):
        """
        Кастомный валидатор, который проверяет существует ли в БД заданное имя пользователя
        :param username: это имя пользователя введенное в поле формы
        :return:
        """
        if username.data != self.original_username:  # сравнивается имя пользователя из поля формы и имя пользователя
                                                    # переданное при инициализации формы. Если пользователь в поле формы
                                                    # изменил имя, то далее выполняется запрос в БД
            user = db.session.scalar(sa.select(User).where(User.username == self.username.data))  # поиск в БД пользователя
                                                    # с тамким же именем
            if user is not None:  # если такое имя пользователя уже есть
                raise ValidationError('Please use a different username!')