import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
    basedir, "..", "take_it_easy_app.db"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
