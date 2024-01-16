from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    category = db.Column(db.String(128), nullable=True)
    summary = db.Column(db.String(256), nullable=False)
    content = db.Column(db.String(512), nullable=False)
    author = db.Column(db.String(64), nullable=False)
    date = db.Column(db.String(64), nullable=False)
    image_url = db.Column(db.String(128), nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    category = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    date = db.Column(db.String(64), nullable=False)
    image_url = db.Column(db.String(128), nullable=False)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    subject = db.Column(db.String(128))
    message = db.Column(db.String(256))

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128))
    website = db.Column(db.String(128))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)