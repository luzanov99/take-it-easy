from flask_sqlalchemy import SQLAlchemy

# TODO set delete behavior
# Add Model Task Status
# Add relationship (User-Task)
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
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
    adress=db.Column(db.String, db.ForeignKey('tasks.id'))
    comment=db.relationship('Comments', backref=db.backref('users'), lazy=True)
    def __repr__(self):
        return f'<User {self.username}>'



class Task(db.Model):
    
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    status = db.relationship('Status', backref=db.backref('tasks'), lazy=True)
    author= db.relationship('User', backref=db.backref('tasks'), lazy=True)
    comment=db.relationship('Comments', backref=db.backref('tasks'), lazy=True)
    executor=db.relationship('User',  lazy=True)
    def __repr__(self):
        return f'<Task {self.title} >'


class Status(db.Model):
    __tablename__ = 'statuses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    task = db.Column(db.String, db.ForeignKey('tasks.title'))
    def __repr__(self):
        return f'<Status {self.name}>'

class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text=db.Column(db.Text, nullable=False)
    date=db.Column(db.DateTime, nullable=False)
    attach=db.Column(db.LargeBinary, nullable=True)
    task =db.Column(db.String, db.ForeignKey('tasks.title'))
    author=db.Column(db.String, db.ForeignKey('users.username'))
    def __repr__(self):
        return f'<Status {self.text}>'


#py = Status(name='Python')
#p = Task(title='Snakes', description='Ssssssss', due_date='12.10.2020',status=[py])
#print(p.due_date)



