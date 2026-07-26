# этот код представляет собой набор модульных тестов (unit tests) для приложения. Он проверяет логику работы модели
# пользователя (User) и системы подписок. Ценность этих тестов в том, что они проверяют работу приложения после внесения
# изменений в него и до его деплоя устранять ошибки
#!/usr/bin/env python
from datetime import  datetime, timezone, timedelta  # для работы с датами и временем
import unittest  # импорт инструментов тестирования
from app import create_app, db # импорт приложения и БД
from app.models import User, Post  # импорт проверяемых классов
from config import Config

class TestConfig(Config):
    """
    Задача этого класса - изоляции тестовой среды от реальной работы приложения (разработки или продакшна). Он переопределяет
    глобальные настройки Flask таким образом, чтобы тесты выполнялись быстро, безопасно и не влияли на настоящие данные.
    """
    TESTING = True  # встроенная маркерная переменная flask указывающая на состояние приложения
    SQLALCHEMY_DATABASE_URI = 'sqlite://' # SQLALCHEMY_DATABASE_URI — это переменная, которая указывает SQLAlchemy (ORM-системе),
                    # к какой именно базе данных нужно подключиться. В выражении 'sqlite://' важно отсутствие имени файла
                    # после двоеточия, это специальный формат подключения к СУБД SQLite. Она означает, что база данных
                    # будет создана in-memory (в оперативной памяти).


class UserModelCase(unittest.TestCase):
    """
    UserModelCase - это кастомный класс, унаследованный из встроенного. Это кастомный тестировщик, он тестирует работу
    методов моделей User и Post из models.py.
    """
    def setUp(self):
        """
        Метод запускается перед каждым тестом, создает новый экземпляр приложения, создает контекст приложения и отправляет
        его в стек потока. Это гарантирует, что экземпляр приложения Flask вместе с его конфигурационными данными будет
        доступен для расширений Flask. Метод также создает чистые таблицы в БД
        :return:
        """
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()  # отправление/запуск контекста приложения
        db.create_all()  # создает таблицы в БД, указанной в конфигурации SQLALCHEMY_DATABASE_URI, на основе моделей описанных в
                        # коде (в данном случае это User и Post)

    def tearDown(self):
        """
        Метод запускается после каждого теста. Удаляет сессию и очищает базу данных, чтобы тесты не влияли друг на друга.
        :return:
        """
        db.session.remove()  # очищает и закрывает текущую сессию взаимодействия с базой данных
        db.drop_all()  # удаление таблиц и все данные из БД
        self.app_context.pop()  # завершение существования контекста приложение, т.е. обратное тому что делает self.app_context.push()

    # дальше начинаются непосредственно тесты
    def test_password_hashing(self):
        """
        Данный тест проверяет соответствие введенного пароля заданному паролю
        :return:
        """
        u = User(username='susan', email='susan@example.com')  # создание пользователя
        u.set_password('cat')  # создание пароля, его хеширование и сохранение в модель
        self.assertFalse(u.check_password('dog'))  # проверяется неверный ввод пароля
        self.assertTrue(u.check_password('cat'))  # проверяется верный ввод пароля

    def test_avatar(self):
        """
        Данный тест проверяет генерацию аватарок через сервис Gravatar. Код сравнивает созданную ссылку с ожидаемой
        (хеш от email).
        :return:
        """
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))  #

    def test_follow(self):
        u1 = User(username='john', email='john@example.com')  # создание пользователя 1 (п1)
        u2 = User(username='susan', email='susan@example.com')  # создание пользователя 2 (п2)
        db.session.add(u1)  # добавление пользователя в БД
        db.session.add(u2)  #
        db.session.commit()  # исполнение выполненных изменений
        following = db.session.scalars(u1.following.select()).all()  # получение из БД списка пользователей на которых подписан пользователь 1
        followers = db.session.scalars(u2.followers.select()).all()  # получение из БД списка пользователей подписанных на пользователя 2
        self.assertEqual(following, [])  # проверяется что п1 не подписан на п2
        self.assertEqual(followers, [])  # проверяется что п2 не имеет подписчика п1

        u1.follow(u2)  # п1 подписывается на п2
        db.session.commit()  # исполнение изменения
        self.assertTrue(u1.is_following(u2))  # проверка что п1 подписан на п2
        self.assertEqual(u1.following_count(), 1)  # проверка что п1 подписан на одного пользователя
        self.assertEqual(u2.followers_count(), 1)  # проверка что у п2 один подписчик
        u1_following = db.session.scalars(u1.following.select()).all()  # получение всех пользователей, на которые подписан п1
        u2_followers = db.session.scalars(u2.followers.select()).all()  # получение всех подписчиков п2
        self.assertEqual(u1_following[0].username, 'susan')  # проверка что п1 подписан на пользователя по имени susan
        self.assertEqual(u2_followers[0].username, 'john')  # проверка что п2 имеет подписчика по имени john

        u1.unfollow(u2)  # п1 отписывается от п2
        db.session.commit()  # исполнение изменений
        self.assertFalse(u1.is_following(u2))  # проверка что п1 не подписан на п2
        self.assertEqual(u1.following_count(), 0)  # проверка что п1 ни на кого не подписан
        self.assertEqual(u2.followers_count(), 0)  #проверка что п2 не имеет подписчиков

    def test_follow_posts(self):
        """
        Метод проверяет правильное получение постов
        :return:
        """
        # создаются 4 пользователя
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])  # все созданные пользователи добавляются в БД

        now = datetime.now(timezone.utc)  # фиксируется время
        # создаются 4 поста
        p1 = Post(body='post from john', author=u1, timestamp=now + timedelta(seconds=1))
        p2 = Post(body='post from susan', author=u2, timestamp=now + timedelta(seconds=4))
        p3 = Post(body='post from mary', author=u3, timestamp=now + timedelta(seconds=3))
        p4 = Post(body='post from david', author=u4, timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])  # все созданные посты добавляются в БД
        db.session.commit()  # исполнение изменений

        u1.follow(u2)  # п1 подписывается на п2
        u1.follow(u4)  # п1 подписывается на п4
        u2.follow(u3)  # п2 подписывается на п3
        u3.follow(u4)  # п3 подписывается на п4
        db.session.commit()  # исполнение изменений

        f1 = db.session.scalars(u1.following_posts()).all()  # получение постов для п1
        f2 = db.session.scalars(u2.following_posts()).all()  # получение постов для п2
        f3 = db.session.scalars(u3.following_posts()).all()  # получение постов для п3
        f4 = db.session.scalars(u4.following_posts()).all()  # получение постов для п4
        self.assertEqual(f1, [p2, p4, p1])  # проверка какие посты получил п1
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])


if __name__ == '__main__':
    unittest.main(verbosity=2)  # verbosity=2 в конце кода заставит Python выводить подробный отчет по каждому тесту

# для запуска тестов в терминале ввести: python tests.py