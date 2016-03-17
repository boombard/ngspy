class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://ge2:123456@localhost/experiments'

class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'postgresql://ge2:123456@localhost/ngspy_test'

