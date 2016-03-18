import json
import unittest

from ngspy.app import create_app
from ngspy.app.config import TestConfig
from ngspy.app.extensions import db
from ngspy.app.db_scripts import db_drop_everything
from ngspy.app.models import *

app = create_app(config=TestConfig)


def resp_data(resp):
    return json.loads(resp.data.decode('utf-8'))


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.app = app
        with app.app_context():
            db.session.flush()
            db.session.rollback()
            db.session.close()
            db.create_all()

    def create_dummy_data(self):
        with app.app_context():
            team = Team(name='test_team')
            db.session.add(team)
            user = User(name='test_user', team=team)
            db.session.add(user)
            organism = Organism(common_name='Mouse', latin_name='M. Musculus')
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            ses = getattr(db, 'session', None)
            if ses is not None:
                db.session.flush()
                db.session.rollback()
                db.session.close()
            db_drop_everything(db)


if __name__ == '__main__':
    unittest.main()

