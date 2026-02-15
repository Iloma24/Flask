# этот файл содержит несколько конфигурационных объекта, унаследованных от базового класса

class BaseConfig(object):
    """Базовый конфигурационный класс"""
    SECRET_KEY = 'A random secret key'
    DEBUG = True
    TESTING = False
    NEW_CONFIG_VARIABLE = 'my value'


class ProductionConfig(BaseConfig):
    """Конфигурационный класс для этапа продакшена"""
    DEBUG = False
    SECRET_KEY = open('/path/to/secret/file').read()


class StagingConfig(BaseConfig):
    """Конфигурационный класс для этапа Staging"""
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    """Конфигурационный класс для этапа Development"""
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'Some secret key'

# чтобы того чтобы задействовать один из этих классов в приложении, нужно соответствующий класс импортировать в файл с
# приложением и настроить следующим кодом: app.config.from_object(configs.DevelopmentConfig)