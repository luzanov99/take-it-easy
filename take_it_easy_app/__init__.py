from take_it_easy_app.models import db 
from flask import Flask, render_template

def create_app():
    app=Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    return app