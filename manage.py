from flask.ext.script import Manager

from app import create_app
from app.extensions import db
from app.config import BaseConfig, TestConfig
from app.db_scripts import db_drop_everything

app = create_app()
manager = Manager(app)


@manager.command
def run():
    app.run()


@manager.command
def test():
    pass


@manager.command
def create_db():
    with app.app_context():
        db.create_all()


@manager.command
def reset_db():
    with app.app_context():
        db_drop_everything(db)
        db.create_all()


if __name__ == '__main__':
    manager.run()

