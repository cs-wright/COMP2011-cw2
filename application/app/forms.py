from flask_wtf import Form
from wtforms import TextField, DateField, SelectField, PasswordField, TextAreaField
from wtforms.validators import DataRequired
from datetime import datetime

class RegisterUser(Form):
    name = TextField('name', validators=[DataRequired()])
    username = TextField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    correctFormat ='%d/%m/%Y'
    dob = DateField('dob', format=correctFormat, validators=[DataRequired()])
    gender = SelectField('gender', choices=['Male', 'Female', 'Other', 'Prefer not to say'], validators=[DataRequired()])

class LoginUser(Form):
    username = TextField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class WritePost(Form):
    txt = TextAreaField('Whats on your mind?', validators=[DataRequired()])