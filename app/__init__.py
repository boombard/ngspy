from flask import Flask
from ngspy.app.config import BaseConfig, TestConfig
from ngspy.app.extensions import db
import ngspy.app.models


def create_app(config=BaseConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    return app

