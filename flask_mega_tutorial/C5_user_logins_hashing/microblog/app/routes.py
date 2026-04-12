# в данном модуле прописаны маршруты/роуты и их отработка. Данный модуль относится к представлению (view)
from flask import render_template, url_for, flash, redirect  # render_template - для выполнения шаблона, url_for для
                                    # работы с сылками, flash для вывода сообщений, redirect для перенаправления
from flask_login import current_user, login_user, logout_user, login_required  # current_user - встроенный атрибут,
                                    # имеющий доступ к данным пользователя (его состояние относительно системы).
                                    # login_user - встроенная функция. Создает сессию, регистрирует состояние пользователя как "авторизованный".
                                    # logout_user - соответственно обрабатывает выход пользователя из системы.
                                    # login_required - декоратор защищающий ендпоинт от просмотра неавторизованным пользователем
import sqlalchemy as sa  # включает в себя функции базы данных общего назначения и классы, такие как типы и помощники по
                                    # построению запросов
from flask import request  # для работы с http-запросами/методами
from urllib.parse import urlsplit  # для разбивки url на логические части


from flask_mega_tutorial.C5_user_logins_hashing.microblog.app import appObj, db  # импорт приложения и модели БД, созданных
                                                                                # в модуле __init__.py
from flask_mega_tutorial.C5_user_logins_hashing.microblog.app.models import User  # модель пользователя
from flask_mega_tutorial.C5_user_logins_hashing.microblog.app.forms import LoginForm  # импорт пользовательского класса
                                                                                    # веб-форм из модуля forms.py
from flask_mega_tutorial.C5_user_logins_hashing.microblog.app.forms import RegistrationForm  # импорт формы для регистрации
                                                                                            # нового пользователя


@appObj.route('/')
@appObj.route('/index')
@login_required  # защищает ендпоинты от просмотра неавторизованными пользователями. Декоратор перехватывает запрос неавторизованного
                # пользователя и перенаправляет его на страницу авторизации, а после авторизации, перенаправит его обратно.
                # Для этого, декоратор добавит в запрос аргумент next. Для данного ендпоинта запрос будет выглядеть следующим
                # образом: /login?next=/index
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


# 1 вариант просто страницы ввода данных
"""@appObj.route('/login')  # страница ввода данных
def login():  # функция просмотра страницы ввода данных
    form = LoginForm()  # создание экземпляра класса для работы с веб-формами
    return render_template('login.html', title='Sign In', form=form)  # функция render_template делает
                            # рендеринг (преобразует шаблон в HTML-страницу). Эта функция принимает имя файла шаблона и
                            # переменный список аргументов шаблона и возвращает тот же шаблон, но со всеми заполнителями
                            # в нем, замененными фактическими значениями. Функция render_template() вызывает движок
                            # шаблонов Jinja, который поставляется в комплекте с фреймворком Flask. Jinja заменяет
                            # блоки {{ ... }} соответствующими значениями, заданными аргументами, приведенными в вызове
                            # render_template()
"""


# 2 вариант функции просмотра с обработкой введенных пользователем данных
@appObj.route('/login', methods=['GET', 'POST'])  # аргумент methods в декораторе сообщает фласк, что эта функция
                                                # просмотра принимает запросы типа GET и POST. GET - это те, которые
                                                # возвращают информацию клиенту (в данном случае веб-браузеру). POST
                                                # обычно используются, когда браузер отправляет данные формы на сервер

def login():
    """
    В данной функции реализована безопасная авторизация пользователя в системе с помощью инструментов расширения Flask-логин
    :return:
    """
    if current_user.is_authenticated:  # если данный пользователь уже авторизован
        return redirect(url_for('index'))  # перенаправляет его на главную страницу (страница приветствия)
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
            flash('Invalid username or password')  # метод flash() выводит пользователю сообщение о несоответствии
            return redirect(url_for('login'))  # перенаправление на страницу авторизации
        login_user(user, remember=form.remember_me.data)  # если имя пользователя и пароль верны, состояние пользователя
                                    # регистрируется как "авторизованный" с помощью встроенной функции login_user
        next_page = request.args.get('next')  # request.args содержит все данные передаваемые клиентом с запросом.
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
            next_page = url_for('index')
        return redirect(next_page)  # перенаправление на главную страницу (страница приветствия)

    return render_template('login.html', title='Sign In', form=form)  # если форма только открыта или
                                    # в ней есть ошибки, код просто показывает страницу login.html, передавая туда объект
                                    # формы и заголовок.


@appObj.route('/logout')
def logout():
    """
    Эта функция просмотра обрабатывает выход пользователя из системы с помощью встроенной функции logout_user
    :return:
    """
    logout_user()
    return redirect(url_for('index'))


@appObj.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # если пользователь уже авторизован, он перенаправляется на главную страницу. current_user это атрибут Flask-Login
        return redirect(url_for('index'))
    form = RegistrationForm()  # если не авторизован, предлагается форма для регистрации

    if form.validate_on_submit():  # если данные введенные в форму валидированы
        user = User(username=form.username.data, email=form.email.data)  # создается новый пользователь по введенным в форму данным
        user.set_password(form.password.data)  # хеширование пароля
        db.session.add(user)  # созданный пользователь добавляется в БД
        db.session.commit()  # завершение сессии
        flash('Congratulations, you are now a registered user!')  # отображение сообщения об успешной регистрации
        return redirect(url_for('login'))  # перенаправление на страницу для входа в систему

    return render_template('register.html', title='Register', form=form)  # вызов шаблона для
                            # регистрации пользователя