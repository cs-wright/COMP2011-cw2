from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

friendship = db.Table('friendships', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), index=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('user.id')))
    #db.UniqueConstraint('user_id', 'friend_id', name='unique_friendships'))#prevents a user from following themself

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    dob = db.Column(db.DateTime)
    gender = db.Column(db.String(20))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    friends = db.relationship('User',
                            secondary=friendship,
                            primaryjoin=id==friendship.c.user_id,
                            secondaryjoin=id==friendship.c.friend_id)

    def setPassword(self, plain_password):
        self.password = generate_password_hash(plain_password)
    
    def validatePassword(self, guess):
        return check_password_hash(self.password, guess)

    def follow(self, friend):
        if friend not in self.friends:
            self.friends.append(friend)
            db.session.commit()

    def unfollow(self, friend):
        if friend in self.friends:
            self.friends.remove(friend)
            db.session.commit()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))