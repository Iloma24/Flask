# это конфигурационный файл, объект класса Config, настраивающий работу фласк-приложения
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'  # в данном коде происходит обращение к переменной
                # окружения CONFIG_SETTINGS, если в переменной окружения не установлен ключ SECRET_KEY (то есть os.environ.get
                # вернул None), код присваивает элементу переменной окружения SECRET_KEY значение по умолчанию: 'you-will-never-guess'
