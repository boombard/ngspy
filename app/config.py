import os
from ngspy import curr_dir

DATA_STORE = os.environ.get('NGSPY_STORE')
if not DATA_STORE:
    DATA_STORE = os.path.join(curr_dir, 'store')

if not os.path.isdir(DATA_STORE):
    os.makedirs(DATA_STORE)


class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://ge2:123456@localhost/experiments'
    DATA_STORE = DATA_STORE


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'postgresql://ge2:123456@localhost/ngspy_test'
    DATA_STORE = DATA_STORE

