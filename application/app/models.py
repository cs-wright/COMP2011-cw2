from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    dob = db.Column(db.DateTime)
    gender = db.Column(db.String(20))