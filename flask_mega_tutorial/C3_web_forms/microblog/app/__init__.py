# задача данного модуля:
# 1 - создать само приложение. 2 - настроить конфигурацию
from flask import Flask
from flask_mega_tutorial.C3_web_forms.microblog.config import Config
appObj = Flask(__name__)  # Переменная __name__ , передаваемая классу Flask, является предопределенной переменной Python,
                            # которой присваивается имя модуля, в котором она используется

appObj.config.from_object(Config)  # с помощью метода from_object происходит прочтение и применение конфигурационного
                                    # файла (config.py), хранящего настройки приложения


# при запуске приложения через терминал, потребуется ввести ключ безопасности, который хранится в конфигурационном файле (config.py)
secret_key = appObj.config['SECRET_KEY']
appObj.config['WTF_CSRF_ENABLED'] = secret_key
# !!! или альтернативный вариант - отключить запрос ключа безопасности, этот вариант допустим ТОЛЬКО НА ЭТАПЕ РАЗРАБОТКИ!!!
# appObj.config["WTF_CSRF_ENABLED"] = False  # !!! отключаются некоторые встроенные проверки безопасности. Это нужно только
            # для разработки и тестирования !!!

from flask_mega_tutorial.C3_web_forms.microblog.app import routes  # модуль routes импортируется внизу, а не сверху как в большинстве
                                                        # случаев, чтобы избежать циклический импорт
"""
Для проверки что все корректно импортировалось (конкретно в слуае этого приложения), нужно в консоли ввести две команды:
1 - from flask_mega_tutorial.C3_web_forms.microblog import app
2 - app.appObj.config['CONFIG_SETTINGS']
"""
