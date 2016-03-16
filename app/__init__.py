from flask import Flask
from app.extensions import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ge2:123456@localhost/experiments'
db.init_app(app)


