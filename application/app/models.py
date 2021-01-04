from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    dob = db.Column(db.DateTime)
    gender = db.Column(db.String(20))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def setPassword(self, plain_password):
        self.password = generate_password_hash(plain_password)
    
    def validatePassword(self, guess):
        return check_password_hash(self.password, guess)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))