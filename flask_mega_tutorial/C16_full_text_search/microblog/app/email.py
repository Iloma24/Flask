# данный файл интегрирует эл. почту в приложение
from flask_mail import Message
from flask import current_app
from threading import Thread  # для работы с потоками (асинхронно)
from app import mail


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
    # далее следуют 3 варианта извлечения объекта приложения и передачи в отдельный поток
    # 1 вариант для версий фласк до Flask 3.x
    # Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()  # создается новый поток.
                        # target=send_async_email — указывает, какую функцию запустить в потоке.
                        # args=(current_app._get_current_object, msg) — передает аргументы для этой функции (само
                        # приложение Flask и сформированное письмо), выражение current_app._get_current_object() извлекает
                        # фактический экземпляр приложения изнутри current_app. .start() — запускает поток. Сразу после
                        # этой команды функция send_email мгновенно завершается, и сайт продолжает работу, пока фоновый
                        # поток отправляет письмо.
    # 2 вариант для версий фласк Flask 3.x и выше
    # Thread(target=send_async_email, args=(current_app.as_wrapped_value(), msg)).start()
    # 3 вариант, предпочтительный, для любых версий фласк
    appObj = current_app._get_current_object()  # явное извлечение текущего экземпляра приложения
    Thread(target=send_async_email, args=(appObj, msg)).start()  # запуск потока, передавая чистый объект приложения

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

