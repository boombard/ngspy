from flask.ext.script import Manager

from app import app
from app.extensions import db
from app.models import *

manager = Manager(app)

@manager.command
def run():
    app.run()

@manager.command
def create_db():
    db.create_all()


if __name__ == '__main__':
    manager.run()
