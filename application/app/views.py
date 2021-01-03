from flask import render_template, flash
from app import app
from .forms import RegisterUser

@app.route('/login', methods=['GET', 'POST'])
def newUser():
    form = RegisterUser()
    if form.validate_on_submit():
        flash('Succesfully received form data. %s, %s, %s, %s, %s'%(form.name.data, form.username.data, form.password.data, form.dob.data, form.gender.data))
    return render_template('login.html',
                           title='Register new user',
                           form=form)

@app.route('/', methods=['GET', 'POST'])
def home():
	home={'description':'Welcome to this application. Please select one of the three available options from the navigation bar.'}
	return render_template('index.html',
						   title="Home",home=home)