from flask_sqlalchemy import SQLAlchemy

# TODO set delete behavior

db = SQLAlchemy()


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(50),
        unique=True, index=True, nullable=False)
    password = db.Column(
        db.String(128),
        nullable=False)
    userpic_url = db.Column(
        db.String(),
        nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'
