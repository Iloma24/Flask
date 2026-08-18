# здесь создается Blueprint-модуль "основной" (main)
from flask import Blueprint

bp = Blueprint('main', __name__)  # 'main' - уникальное имя Blueprint-элемента/модуля. __name__ — это специальная
                                        # переменная Python. Она указывает Flask текущий модуль, чтобы он понимал, где
                                        # физически на диске искать шаблоны или статические файлы для этого Blueprint.

from app.main import routes  # импорт маршрутов для данного модуля
