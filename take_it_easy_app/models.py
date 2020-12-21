from flask_sqlalchemy import SQLAlchemy

# TODO set delete behavior
# Add Model Task Status
# Add relationship (User-Task)
db = SQLAlchemy()
tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('page_id', db.Integer, db.ForeignKey('task.id'))
)

class User(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True)
    username = db.Column(
        db.String(50),
        unique=True, index=True, nullable=False)
    password = db.Column(
        db.String(128),
        nullable=False)
    userpic_url = db.Column(
        db.String(),
        nullable=True)
    adress = db.Column(db.String, db.ForeignKey('task.id'))
    comment = db.relationship('Comment', backref=db.backref('user'), lazy=True)
    def __repr__(self):
        return f'<User {self.username}>'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.Integer, db.ForeignKey('status.id'))
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor = db.relationship('User',  backref=db.backref('task') ,lazy=True)
    tag = db.relationship('Tag', secondary=tags, backref=db.backref('task_tag'), lazy=True)
    def __repr__(self):
        return f'<Task {self.title} >'


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    task = db.Column(db.Integer, db.ForeignKey('task.id'))

    def __repr__(self):
        return f'<Status {self.name}>'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    attach = db.Column(db.LargeBinary, nullable=True)
    task = db.Column(db.Integer, db.ForeignKey('task.id'))
    author = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Status {self.text}>'

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    task = db.relationship('Task', backref=db.backref('project') ,lazy=True)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)