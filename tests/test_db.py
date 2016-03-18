from __future__ import print_function

import unittest

from ngspy.tests import BaseTest
from ngspy.app.extensions import db
from ngspy.app.models import *


class TestDB(BaseTest):

    def test_dummy_data(self):
        self.create_dummy_data()
        with self.app.app_context():
            user = db.session.query(User).first()
            assert user.team.name == 'test_team', 'Relationship did not load'


if __name__ == '__main__':
    unittest.main()

