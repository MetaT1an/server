from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    pwdhash = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


class Policy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pname = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(100), unique=False, nullable=True)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False)
    tname = db.Column(db.String(35), nullable=False)
    date = db.Column(db.String(20))
    status = db.Column(db.Integer)      # 0 for undo, 1 for running, 2 for completed


class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tid = db.Column(db.Integer)     # task id, define while creating
    hname = db.Column(db.String(35), nullable=False)    # task name
    status = db.Column(db.String(15))
    policy = db.Column(db.String(15))   # define while creating
    start = db.Column(db.String(20))
    end = db.Column(db.String(20))
    elapse = db.Column(db.String(15))
    target = db.Column(db.String(20))   # define while creating
    critical = db.Column(db.Integer)
    high = db.Column(db.Integer)
    medium = db.Column(db.Integer)
    low = db.Column(db.Integer)
    info = db.Column(db.Integer)
