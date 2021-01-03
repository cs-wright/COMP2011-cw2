from flask import render_template, flash
from app import app
from .forms import RegisterUser, LoginUser

@app.route('/auth', methods=['GET', 'POST'])
def authenticate():
    register_form = RegisterUser()
    login_form = LoginUser()
    return render_template('auth.html', 
                            title='Authentication', 
                            register_form=register_form, 
                            login_form=login_form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterUser()
    login_form = LoginUser()

    if register_form.validate_on_submit():
        flash('Succesfully received form data. %s, %s, %s, %s, %s'%(register_form.name.data, register_form.username.data, register_form.password.data, register_form.dob.data, register_form.gender.data))
    return render_template('auth.html', 
                            title='Authentication', 
                            register_form=register_form, 
                            login_form=login_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    register_form = RegisterUser()
    login_form = LoginUser()

    if login_form.validate_on_submit():
        flash('Succesfully received form data. %s, %s'%(login_form.username.data, login_form.password.data))
    return render_template('auth.html', 
                            title='Authentication', 
                            register_form=register_form, 
                            login_form=login_form)



@app.route('/', methods=['GET', 'POST'])
def home():
	home={'description':'Welcome to this application. Please select one of the three available options from the navigation bar.'}
	return render_template('index.html',
						   title="Home",home=home)

