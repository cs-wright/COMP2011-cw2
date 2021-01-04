from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'authenticate'

admin = Admin(app,template_mode='bootstrap3')

migrate = Migrate(app, db)

from app import views, models