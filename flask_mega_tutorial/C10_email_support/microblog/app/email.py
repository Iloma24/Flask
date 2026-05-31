# данный файл интегрирует эл. почту в приложение
from flask_mail import Message
from flask import render_template
from threading import Thread  # для работы с потоками (асинхронно)
from app import mail
from app import appObj



def send_password_reset_email(user):
    """
    Функция отправки по электронной почте инструкции и токена для сброса пароля. Данная функция работает через исполнение двух других
    функций: 1 - get_reset_password_token() генерирует токен и 2 - send_email() отправляет письма. Примечательный момент
    в этой функции: текст и HTML-контент для электронных писем генерируются из шаблонов с использованием функции
    render_template(). Шаблоны получают пользователя и токен в качестве аргументов, так что можно сгенерировать
    персонализированное сообщение электронной почты.
    :param user: пользователь которому отправляется эл. письмо
    :return:
    """
    token = user.get_reset_password_token()  # генерация токена
    send_email(
        '[Microblog] Reset your password',  # заголовок письма
        sender=appObj.config['ADMINS'][0],  # отправитель письма
        recipients=[user.email],  # получатель письма
        # далее функция render_template собирает текст письма из шаблонов, подставляя туда живые данные (объект пользователя
        # user и сгенерированный token)
        text_body=render_template('email/reset_password.txt',
                                  user=user, token=token),  # текстовой формат письма. В качестве текста письма используется текстовый файл
        html_body=render_template('email/reset_password.html',
                                  user=user, token=token)  # HTML-формат письма, используется HTML-шаблон
    )  # отправка письма с инструкцией и токеном


# отправка письма асинхронно, с использованием потока (Thread)
def send_async_email(appObj, msg):
    """
    функция, которая будет выполняться внутри нового потока. Она принимает объект Flask-приложения (app) и объект
    сообщения (msg).
    :param appObj: объект Flask-приложения
    :param msg: собщение
    :return:
    """
    with appObj.app_context():  # Этот контекстный менеджер создает контекст приложения и принудительно «вводит» поток внутрь
                                # окружения Flask, чтобы объекты переданные в новый поток понимали с каким приложением
                                # они работают, например чтобы расширение Flask-Mail могло прочитать настройки (SMTP-сервер,
                                # логин, пароль) из appObj.config.
        mail.send(msg)  # физическая отправка письма через SMTP-клиент


def send_email(subject, sender, recipients, text_body, html_body):
    """
    Эта функция создает новый поток и внутри этого потока отправляет письма.
    :param subject: тема/заголовок письма
    :param sender: отправитель
    :param recipients: получатели
    :param text_body: текст письма в текстовом формате
    :param html_body: текст письма в html-формате
    :return:
    """
    msg = Message(subject, sender=sender, recipients=recipients)  # создается объект письма (тема, отправитель, получатели).
    msg.body = text_body  # текст письма в текстовом формате
    msg.html = html_body  # текст письма в html-формате
    Thread(target=send_async_email, args=(appObj, msg)).start()  # создается новый поток. target=send_async_email — указывает,
                        # какую функцию запустить в потоке. args=(app, msg) — передает аргументы для этой функции (само
                        # приложение Flask и сформированное письмо). .start() — запускает поток. Сразу после этой команды
                        # функция send_email мгновенно завершается, и сайт продолжает работу, пока фоновый поток отправляет письмо.

# отправка письма без использования потока (Thread)
'''
def send_email(subject, sender, recipients, text_body, html_body):
    """
    Это функция-помощник для отправки электронных писем в веб-приложении с использованием расширения Flask-Mail. Она
    собирает все необходимые данные (тему, отправителя, получателей и текст) в один объект и отправляет его через
    настроенный почтовый сервер.
    :param subject: тема письма
    :param sender: отправитель
    :param recipients: получатель/и
    :param text_body: текст письма
    :param html_body: текст письма в виде шаблона (опционально)
    :return: None
    """
    msg = Message(subject, sender=sender, recipients=recipients)  # настройка отправляемого письм: 1 параметр - заголовок
                                                                # письма; 2 - отправитель письма; 3 - получатель
    msg.body = text_body  # текст письма
    msg.html = html_body  # HTML-версия содержания письма (опционально)
    mail.send(msg)  # отправление письма

'''

