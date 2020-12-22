from flask import Flask

from take_it_easy_app.models import db


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    return app
