from flask import render_template, flash, redirect, url_for
from app import app, db, models, admin
from flask_login import current_user, login_user, logout_user, login_required
from .forms import RegisterUser, LoginUser, WritePost
from app.models import User, Post
from flask_admin.contrib.sqla import ModelView 

admin.add_view(ModelView(Post, db.session))

@app.route('/auth', methods=['GET', 'POST'])
def authenticate():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
        #flash('Succesfully received form data. %s, %s, %s, %s, %s'%(register_form.name.data, register_form.username.data, register_form.password.data, register_form.dob.data, register_form.gender.data))
        user = User.query.filter_by(username=register_form.username.data).first()
        if user is not None:
            flash('This username is already in use!')
        else:
            n=register_form.name.data
            u=register_form.username.data
            p=register_form.password.data
            d=register_form.dob.data
            g=register_form.gender.data
            account = User(name=n, username=u, dob=d, gender=g)
            account.setPassword(p)
            db.session.add(account)
            db.session.commit()
            flash('registered successfully')
    return render_template('auth.html', 
                            title='Authentication', 
                            register_form=register_form, 
                            login_form=login_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    register_form = RegisterUser()
    login_form = LoginUser()

    if login_form.validate_on_submit():
        #flash('Succesfully received form data. %s, %s'%(login_form.username.data, login_form.password.data))
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None:
            flash('Invalid username!')
        elif user.validatePassword(login_form.password.data) == False:
            flash('Wrong Password!')
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template('auth.html', 
                            title='Authentication', 
                            register_form=register_form, 
                            login_form=login_form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authenticate'))


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    form = WritePost()
    home={'description':'Welcome to this application. Please select one of the three available options from the navigation bar.'}
    if form.validate_on_submit():
        flash('posted!')
        new = Post(content=form.txt.data, author=current_user)
        db.session.add(new)
        db.session.commit()
    return render_template('index.html', title="Home", home=home, form=form)


@app.route('/myposts', methods=['GET', 'POST'])
@login_required
def myposts():
    posts = Post.query.filter_by(author_id=current_user.id)
    return render_template('myposts.html', title="My Posts", posts=posts)


@app.route('/delete_post/<id>', methods=['GET'])
@login_required
def delete_post(id):
    post = Post.query.get(id)
    if current_user.id == post.author_id:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted!')
    else:
        flash('You do not have permission to delete another users posts!')
    return redirect('/myposts')