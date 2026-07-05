# в данном файле показано создание кастомных консольных команд конкретно для этого приложения. Эти команды которые запускают команды
# pybabel со всеми аргументами, специфичными для данного приложения.
from app import appObj  # импорт приложения
import os  # для взаимодействия с операционной системой (вызов терминальных команд, удаление файлов)
import click # пакет для создания консольных команд

@appObj.cli.group() # декоратор используемый для создания группы команд. Все подкоманды будут вызываться через префикс
                    # flask translate ...
def translate():  # Это корневая (родительская) функция. Название коман происходит от названия декорированной (корневой)
                # функции, и она содержит только строку документации. Имя функции translate становится именем команды в
                # консоли. Функция пустая (pass), так как она служит лишь «контейнером» для подкоманд.
    """Translation and localization commands."""  # эта информация будет возвращена при вводе команды: flask translate --help
    pass


@translate.command()  # Декоратор регистрирует функцию ниже как подкоманду внутри группы translate. В консоли она будет
                        # вызываться как flask translate update.
def update():  # функция update() объединяет шаги extract и update в одной команде, и если все прошло успешно, она удаляет
                # файл messages.pot после завершения обновления.
    """Update all languages."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):  # os.system выполняет консольную команду для
                    # извлечения (сбора) строк для перевода из исходного кода. os.system возвращает 0, если команда выполнена
                    # успешно, и код ошибки (не ноль), если произошел сбой.
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i messages.pot -d app/translations'):  # эта команда выполняет обновление уже существующих
                    # .po-файлов перевода, добавляя туда новые найденные строки из шаблона messages.pot.
        raise RuntimeError('update command failed')  # если команда вернула код ошибки (не ноль)
    os.remove('messages.pot')  # если обе команды выполнились без ошибки, шаблон с текстами для перевода удаляется


@translate.command()  # Регистрирует подкоманду компиляции (flask translate compile).
def compile():  # Функция, переводящая текстовые .po файлы в бинарные .mo файлы (которые и читает Flask во время работы).
    """Compile all languages."""
    if os.system('pybabel compile -d app/translations'):  # Запускает компиляцию всех языковых пакетов, находящихся по
                                                        # пути app/translations
        raise RuntimeError('compile command failed')


@translate.command()  # Регистрирует подкоманду инициализации нового языка (flask translate init <код_языка>).
@click.argument('lang')  # Объявляет обязательный аргумент строки для CLI. Click перехватит введенное пользователем
                        # слово (например, ru или es) и передаст его в функцию init(lang) в качестве переменной lang.
def init(lang):  # Функция инициализации, принимающая аргумент lang. Команда init принимает код нового языка в качестве аргумента.
    """Initialize a new language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):  # перед созданием нового языка заново сканирует
                                                                        # проект и создает актуальный шаблон messages.pot
        raise RuntimeError('extract command failed') # если выполненная команда возвратила код ошибки (не  ноль)
    if os.system(
            'pybabel init -i messages.pot -d app/translations -l ' + lang):  # Запускает команду pybabel init. Флаг -l
                        # принимает переданную строку lang (например, ru), создавая структуру папок вроде app/translations/ru/LC_MESSAGES/messages.po
        raise RuntimeError('init command failed')  # вызывается исключение, если не удалось создать структуру для нового
                        # языка (например, если такой язык уже существует)
    os.remove('messages.pot')  # если обе команды выполнились без ошибок, то ставший ненужным временный файл messages.pot удаляется