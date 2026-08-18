# здесь прописываются маршруты обрабатывающие авторизацию
from flask import render_template, url_for, flash, redirect  # render_template - для выполнения шаблона, url_for для
                                    # работы с сылками, flash для вывода сообщений, redirect для перенаправления
from flask_babel import _  # _ - переводит текст на предпочитаемы пользователем язык
from flask_login import current_user, login_user, logout_user  # current_user - встроенный атрибут,
                                    # имеющий доступ к данным пользователя (его состояние относительно системы).
                                    # login_user - встроенная функция. Создает сессию, регистрирует состояние пользователя как "авторизованный".
                                    # logout_user - соответственно обрабатывает выход пользователя из системы.

import sqlalchemy as sa  # включает в себя функции базы данных общего назначения и классы, такие как типы и помощники по
                                    # построению запросов
from flask import request  # для работы с http-запросами/методами
from urllib.parse import urlsplit  # для разбивки url на логические части
from app import db  # импорт модели БД, созданной в модуле __init__.py
from app.models import User  # модель пользователя
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, \
                       ResetPasswordForm  # LoginForm - импорт пользовательского класса веб-форма входа в систему;
                            # RegistrationForm - форма для регистрации нового пользователя;
                            # ResetPasswordRequestForm - форма запроса сброса пароля; ResetPasswordForm - форма сброса пароля

from app.auth.email import send_password_reset_email
from app.auth import bp

@bp.route('/login', methods=['GET', 'POST'])  # аргумент methods в декораторе сообщает фласк, что эта функция
                                                # просмотра принимает запросы типа GET и POST. GET - это те, которые
                                                # возвращают информацию клиенту (в данном случае веб-браузеру). POST
                                                # обычно используются, когда браузер отправляет данные формы на сервер
def login():
    """
    В данной функции реализована безопасная авторизация пользователя в системе с помощью инструментов расширения Flask-логин
    :return:
    """
    if current_user.is_authenticated:  # если данный пользователь уже авторизован
        return redirect(url_for('main.index'))  # перенаправляет его на главную страницу (страница приветствия)
    form = LoginForm()  # создание формы авторизации, экземпляра класса для работы с веб-формами
    if form.validate_on_submit():  # метод validate_on_submit() выполняет всю работу по обработке форм. Если выполняется
                                    # GET-запрос, то данный метод пропустит запрос без проверки (там нет форм) и браузер
                                    # вернет страницу с полями для заполнения. Если же выполняется POST-запрос, то метод
                                    # проверит все ли поля заполнены (валидация), если все правильно, выполняется код
                                    # внутри блока if
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)) # из модели БД запрашиваются данные на пользователя
                                    # внесенные в форму авторизации. Используется db.session.scalar а не scalars поскольку
                                    # ожидается, что по введенным данным будет возращен либо 1 пользователь либо 0, если
                                    # ожидается множество объектов, то используется scalars. sa - инструмент для формиро-
                                    # вания запроса
        if user is None or not user.check_password(form.password.data):  # если такого пользователя нет или пароль не
                                    # соответствует хешу пароля
            flash(_('Invalid username or password'))  # метод flash() выводит пользователю сообщение о несоответствии
            return redirect(url_for('auth.login'))  # перенаправление на страницу авторизации
        login_user(user, remember=form.remember_me.data)  # если имя пользователя и пароль верны, состояние пользователя
                                    # регистрируется как "авторизованный" с помощью встроенной функции login_user
        next_page = request.args.get('next')  # request.args дает доступ к данным передаваемые клиентом с запросом в адресной строке.
                                    # Извлечение ендпоинта куда пытался перейти неавторизованный пользователь и
                                    # добавление к нему аргумента next. Аргумент next содержит ендпоинт куда пытался перейти
                                    # неавторизованный пользователь. Например если пользователь пытался перейта на главную
                                    # страницу (index), сформированный ендпоинт будет выглядеть так - /login?next=/index
        if not next_page or urlsplit(next_page).netloc != '':  # функция urlsplit() разбивает (на кортеж) полный адрес по аргументам
                                    # из которых адрес состоит. Здесь проверяется не ведет ли ссылка на сторонний вредоносный
                                    # сайт. Если параметр next пустой или ссылка внешняя, пользователя отправляют на
                                    # главную страницу (index). Значение urlsplit(next_page).netloc всегда будет пустым,
                                    # если попытка перехода была в пределах сайта. Если же кто-то подставляет внешнюю ссылку,
                                    # например, http://vzlom.com то значение будет vzlom.com
            next_page = url_for('main.index')
        return redirect(next_page)  # перенаправление на главную страницу (страница приветствия)

    return render_template('auth/login.html', title=_('Sign In'), form=form)  # если форма только открыта или
                                    # в ней есть ошибки, код просто показывает страницу login.html, передавая туда объект
                                    # формы и заголовок.


@bp.route('/logout')
def logout():
    """
    Эта функция просмотра обрабатывает выход пользователя из системы с помощью встроенной функции logout_user
    :return:
    """
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Эта функция просмотра. Проверяет что пользователь, вызывающий этот маршрут, не вошел в систему. Форма обрабатывается
    так же, как и форма для входа в систему. Логика, выполняемая внутри условия if validate_on_submit(), создает нового
    пользователя с указанным именем пользователя, электронной почтой и паролем, записывает его в базу данных, а затем
    перенаправляет на приглашение для входа, чтобы пользователь мог войти в систему.
    :return:
    """
    if current_user.is_authenticated:  # если пользователь уже авторизован, он перенаправляется на главную страницу. current_user это атрибут Flask-Login
        return redirect(url_for('main.index'))
    form = RegistrationForm()  # если не авторизован, предлагается форма для регистрации

    if form.validate_on_submit():  # если данные введенные в форму валидированы
        user = User(username=form.username.data, email=form.email.data)  # создается новый пользователь по введенным в форму данным
        user.set_password(form.password.data)  # хеширование пароля
        db.session.add(user)  # созданный пользователь добавляется в БД
        db.session.commit()  # завершение сессии
        flash(_('Congratulations, you are now a registered user!'))  # отображение сообщения об успешной регистрации
        return redirect(url_for('auth.login'))  # перенаправление на страницу для входа в систему

    return render_template('auth/register.html', title=_('Register'), form=form)  # вызов шаблона для
                            # регистрации пользователя



@bp.route('/reset_password_request', methods=['GET', 'POST'])  # страница СОЗДАНИЯ запроса на сброс пароля, ещё не сброс пароля
def reset_password_request():
    """
    Эта функция просмотра обрабатывает страницу создания запроса сброса пароля. Это ещё не сброс пароля. Сброс пароля
    обрабатывает другая функция просмотра
    :return:
    """
    if current_user.is_authenticated:  # если текущий пользователь авторизован
        return redirect(url_for('main.index'))  # пользователь перенаправляется на главную страницу
    form = ResetPasswordRequestForm()  # содается форма для запроса сброса пароля
    if form.validate_on_submit():  # метод validate_on_submit() выполняет всю работу по обработке форм. Если выполняется
                                    # GET-запрос, то данный метод пропустит запрос без проверки (там нет форм) и браузер
                                    # вернет страницу с полями для заполнения. Если же выполняется POST-запрос, то метод
                                    # проверит все ли поля заполнены (валидация), если все правильно, выполняется код
                                    # внутри блока if
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))  # проверяется есть ли в БД имейл
                                    # введенный в форму для запроса сброса пароля
        if user:  # если такой имейл есть
            send_password_reset_email(user)  # функция отправляет пользователю на почту письмо
        flash(_('Check your email for the instructions to reset your password'))  # вывод информационного сообщения в браузер
        return redirect(url_for('auth.login'))  # пользователь перенаправляется на страницу авторизации
    return render_template('auth/reset_password_request.html', title=_('Reset Password'), form=form)  # если
                                    # форма еще не отправлена (или заполнена с ошибками), код отображает HTML-страницу
                                    # reset_password_request.html


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])  # страница сброса пароля
def reset_password(token):
    """
    Эта функция просмотра проверяет действительность переданного токен и в случае его действительности, позволяет ввести
    в форму ноый пароль
    :param token:
    :return:
    """
    if current_user.is_authenticated:  # если пользователь авторизован, сброс пароля невозможен
        return redirect(url_for('main.index'))  # пользователь перенаправляется на главную страницу
    user = User.verify_reset_password_token(token)  # проверка токена и получение дпнных пользователя
    if not user:  # если токен не действительный
        return redirect(url_for('main.index'))  # пользователь перенаправляется на главную страницу
    form = ResetPasswordForm()  # создается форма для ввода нового пароля
    if form.validate_on_submit():  # если форма проходит валидацию
        user.set_password(form.password.data)  # устанавливается новый пароль
        db.session.commit()  # сохранение изменений
        flash(_('Your password has been reset!'))  # информационное сообщение
        return redirect(url_for('auth.login'))  # перенаправление на страницу авторизации
    return render_template('auth/reset_password.html', form=form)  # вызов шаблона ввода нового пароля