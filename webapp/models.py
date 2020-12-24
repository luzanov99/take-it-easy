from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
tags = db.Table(
    "tags",
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")),
    db.Column("page_id", db.Integer, db.ForeignKey("task.id")),
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(50), unique=True, index=True, nullable=False
    )
    password = db.Column(db.String(128), nullable=False)
    userpic_url = db.Column(db.String(), nullable=True)
    comment = db.relationship("Comment", backref=db.backref("user"), lazy=True)
    role =db.Column(db.String(10), index=True)
    
    def set_password(self, password):
        self.password=generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        
        return self.role =='admin'

    def __repr__(self):
        return f"<User {self.username}>"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    author = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor = db.Column(db.Integer, db.ForeignKey("user.id"))
    task_author = db.relationship("User", foreign_keys=[author])
    task_executor = db.relationship("User", foreign_keys=[executor])
    project = db.Column(db.Integer, db.ForeignKey("project.id"))
    status = db.Column(db.Integer, db.ForeignKey("status.id"))
    tag = db.relationship(
        "Tag", secondary=tags, backref=db.backref("task_tag"), lazy=True
    )

    def __repr__(self):
        return f"<Task {self.title} >"


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    task = db.Column(db.Integer, db.ForeignKey("task.id"))

    def __repr__(self):
        return f"<Status {self.name}>"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    attach = db.Column(db.LargeBinary, nullable=True)
    task = db.Column(db.Integer, db.ForeignKey("task.id"))
    author = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Comment {self.text}>"


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    tasks = db.Column(db.Integer, db.ForeignKey("task.id"))

    def __repr__(self):
        return f"<Project {self.name}>"


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Tag {self.name}>"
