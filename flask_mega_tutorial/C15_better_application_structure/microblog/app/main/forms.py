# здесь создаются несколько форм: форма для редактирования профиля; пустая форма; форма отправки поста
from flask_wtf import FlaskForm  # импорт базового встроенного класса вэб-формам
from wtforms import StringField, SubmitField  # импорт встроенных полей
from wtforms import TextAreaField  # многострочное текстовое поле
from wtforms.validators import DataRequired, ValidationError, Length  # импорт валидаторов ввода значений в поля
                            # для регистрации. Length - валидатор длинны строки
from flask_babel import _, lazy_gettext as _l  # импорт дфух встроенных функций для перевода текстовых сообщений: _ и _l.
                                              # lazy_gettext - функция "ленивого" перевода, т.е. переводит тексты, в
                                              # которых присутствуют динамические фрагменты, например значения вврдимые
                                              # пользователем, поэтому она выполняет т.н. отложенный перевод уже после
                                              # рендеринга шаблона
import sqlalchemy as sa  # для работы с БД (запросы, функции и т.д.)
from app import db  # импорт БД
from app.models import User  # импорт модели таблицы Пользователи


class EditProfileForm(FlaskForm):
    """
    Это класс редактора профиля пользователя (форма). Состоит из нескольких полей для заполнения. Задача этого класса -
    создать форму для редактирования профиля с «умной» проверкой уникальности имени. Главная проблема, которую он решает:
    как не выдавать ошибку «это имя уже занято», когда пользователь сохраняет свое же текущее имя.
    """
    username = StringField(_l('Username'), validators=[DataRequired()])  # настройка поля "имя пользователя"
    about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=140)])  # настройка поля "о себе".
                                # TextAreaField - многострочное поле. Валидатор Length - проверяет соблюдение заданной
                                # длинны строки (измерение в символах)
    submit = SubmitField(_l('Submit'))

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
                raise ValidationError(_('Please use a different username!'))


class EmptyForm(FlaskForm):
    """
    Данный класс представляет пустую форму (кнопку) со скрытым CSRF-токеном для оформления подписки/отписки пользователя
    """
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    """
    Этот класс представляет из себя - форму для отправки сообщений в блог
    """
    post = TextAreaField(_l('Say something'), validators=[DataRequired(), Length(min=1, max=140)])  # поле для ввода сообщения
    submit = SubmitField(_l('Submit'))  # подтверждение отправки сообщения
