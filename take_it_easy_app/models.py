from flask_sqlalchemy import SQLAlchemy

# TODO check/add relationships between tables
# TODO add helper table to represent Many-to-many (Task-Tag):
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/?highlight=lazy#many-to-many-relationships
# TODO add uselist attr to model to represent One-to-one:
# (Task-Status, Comment-User)
# TODO set delete behavior
# TODO optional: set lengths of string fields if sqlite3 allows it

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    userpic_url = db.Column(db.String, nullable=True)
    # email and telegram_username are optional so far
    email = db.Column(db.String, unique=True, nullable=True)
    telegram_username = db.Column(db.String, unique=True, nullable=True)

    tasks = db.relationship('Task', backref='user', lazy=True)
    roles = db.relationship('Role', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
        )
    permissions = db.relationship(
        'Permission',
        backref=db.backref('role'),
        lazy=True
        )

    def __repr__(self):
        return f'<Role {self.name}>'


class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    # do we need action_granted here?
    action_granted = db.Column(db.String, unique=True, nullable=False)

    project = db.relationship(
        'Project',
        backref=db.backref('permission'),
        lazy=True
        )
    project_id = db.Column(
        db.Integer,
        db.ForeignKey('project.id'),
        nullable=False
        )

    def __repr__(self):
        return f'<Permission {self.action_granted}>'


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=True)
    status = db.Column(db.String, nullable=False)

    tasks = db.relationship('Task', backref='project', lazy=True)

    def __repr__(self):
        return f'<Project {self.name}>'


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    created_at = db.Column(db.Datetime, nullable=False)
    due_date = db.Column(db.Datetime, nullable=True)

    project_id = db.Column(
        db.Integer,
        db.ForeignKey('project.id'),
        nullable=False
        )
    author_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
        )
    assignee_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=True
        )
    status = db.relationship(
        'Status',
        backref=db.backref('task'),
        lazy=True
        )
    tags = db.relationship(
        'Tag', backref=db.backref('task'),
        lazy=True
        )

    def __repr__(self):
        return f'<Task {self.title} >'


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=True)

    task_id = db.Column(
        db.Integer,
        db.ForeignKey('task.id'),
        nullable=False
        )

    def __repr__(self):
        return f'<Tag {self.name}>'


class Status(db.Model):
    __tablename__ = 'statuses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    task_id = db.Column(
        db.Integer,
        db.ForeignKey('task.id'),
        nullable=False
        )

    def __repr__(self):
        return f'<Status {self.name}>'


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    published_at = db.Column(db.Datetime, nullable=False)
    attachments = db.relationship(
        'Attachment',
        backref='comment',
        lazy=True
        )
    task_id = db.Column(
        db.Integer,
        db.ForeignKey('task.id'),
        nullable=False
        )
    author_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
        )

    def __repr__(self):
        return f'<Comment {self.text}>'


class Attachment(db.Model):
    __tablename__ = 'attachments'

    id = db.Column(db.Integer, primary_key=True)
    file_url = db.Column(db.String, nullable=False)

    comment_id = db.Column(
        db.Integer,
        db.ForeignKey('comment.id'),
        nullable=False
        )

    def __repr__(self):
        return f'<Attachment {self.file_url}>'
