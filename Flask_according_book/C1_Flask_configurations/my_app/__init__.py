# в данном файле создается фласк приложение и выполняется регистрация Blueprint-модуля
from flask import Flask
from Flask_according_book.C1_Flask_configurations.my_app.hello.views import hello  # импортируется Blueprint-модуль где
                                                                                    # прописана маршрутизация

app = Flask(__name__)  # создание приложения
app.register_blueprint(hello)  # внутри приложения регистрируется импортированный Blueprint-модуль
