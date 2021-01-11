from flask import render_template, flash, redirect, url_for
from app import app, db, models, admin
from flask_login import current_user, login_user, logout_user, login_required
from .forms import RegisterUser, LoginUser, WritePost, UpdatePassword
from app.models import User, Post, friendship
from flask_admin.contrib.sqla import ModelView 
#from datetime import datetime

from sqlalchemy.orm import aliased


#admin.add_view(ModelView(Post, db.session))
#admin.add_view(ModelView(User, db.session))
@app.route('/auth', methods=['GET', 'POST'])
def authenticate():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    register_form = RegisterUser()
    login_form = LoginUser()
    home={'description':'Welcome to trial of our new social network designed to keep people connected and up to date! Please look either register or login by filling out the forms below. We hope your improved social experience!'}
    return render_template('auth.html', 
                            title='Authentication',
                            home=home, 
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
    
    home={'description':'Welcome to trial of our new social network designed to keep people connected and up to date! Please look either register or login by filling out the forms below. We hope your improved social experience!'}
    return render_template('auth.html', 
                            title='Authentication', 
                            home=home, 
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
    home={'description':'Welcome to trial of our new social network designed to keep people connected and up to date! Please look either register or login by filling out the forms below. We hope your improved social experience!'}
    return render_template('auth.html', 
                            title='Authentication', 
                            home=home, 
                            register_form=register_form, 
                            login_form=login_form)


@app.route('/manageaccount', methods=['GET','POST'])
@login_required
def accountManagement():
    form = RegisterUser()
    passwordForm = UpdatePassword()
    if form.name.data is None:
        form.name.data = current_user.name

    if form.username.data is None:
        form.username.data = current_user.username

    if form.dob.data is None:
        form.dob.data = current_user.dob
    form.password.data = current_user.password
    if form.gender.data is None:
        form.gender.data = current_user.gender

    if form.validate_on_submit():
        current_user.name = form.name.data

        count=0
        if current_user.username != form.username.data:
            for user in User.query.all():
                if user.username == form.username.data:
                    count+=1
            if count > 0:
                #Username is already taken
                form.username.data = current_user.username
                flash('This Username is taken!')
            else:
                #username is available
                current_user.username = form.username.data

        current_user.dob = form.dob.data
        current_user.gender = form.gender.data
        flash('Account updated!')
        db.session.commit()
    
    if passwordForm.validate_on_submit():
        if current_user.validatePassword(passwordForm.current_password.data):
            if passwordForm.new_password.data == passwordForm.confirm_password.data:
                current_user.setPassword(passwordForm.new_password.data)
                flash('Password Updated!')
            else:
                flash('Passwords did not match!')
        else:
            flash('Wrong Password!')

    return render_template('accountmanagement.html',
                           title='Manage Account',
                           form=form, 
                           passwordForm=passwordForm)


@app.route('/logout')
@login_required
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


@app.route('/followingposts', methods=['GET', 'POST'])
@login_required
def followingposts():
    # posts = Post.query.join(friendship, (friendship.c.friend_id == Post.author_id)).filter(friendship.c.user_id == current_user.id).order_by(Post.date.desc())
    # followingposts = []
    # for entry in posts:
    #     temp = User.query.get(entry.author_id)
    #     #followingposts.append(entry & temp.name)
    #     dictionary = {'date':entry.date, 'content':entry.content, 'name':temp.name}
    #     followingposts.append(dictionary)
    followingposts=current_user.following_posts()
    return render_template('followingposts.html', title="Following users Posts", posts=followingposts)

@app.route('/myposts', methods=['GET', 'POST'])
@login_required
def myposts():
    posts = Post.query.filter_by(author_id=current_user.id)
    return render_template('myposts.html', title="My Posts", posts=posts)


@app.route('/edit_post/<id>', methods=['GET','POST'])
@login_required
def edit_post(id):
    post = Post.query.get(id)
    form = WritePost()
    if form.txt.data is None:
        form.txt.data = post.content
    if form.validate_on_submit():
        post.content = form.txt.data
        #post.date = datetime.utcnow
        db.session.commit()
        return redirect('/myposts')

    return render_template('edit_post.html',
                           title='Edit Post',
                           form=form)


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

@app.route('/following', methods=['GET', 'POST'])
@login_required
def following():
    following = current_user.friends
    return render_template('following.html', title="All Users", users=following)


@app.route('/unfollow/<id>', methods=['GET'])
@login_required
def unfollow(id):
    following = User.query.get(id)
    current_user.unfollow(following)
    flash('Unfollowed!')
    return redirect('/following')


@app.route('/followers', methods=['GET', 'POST'])
@login_required
def followers():
    # user_id = current_user.id

    # UserAlias = aliased(User)
    # followers = User.query.join(UserAlias.friends).with_entities(UserAlias).filter_by(id=current_user.id)
    followers=current_user.following_user()
    return render_template('followers.html', title="Followers", users=followers)

@app.route('/rmfollower/<id>', methods=['GET'])
@login_required
def remove_follower(id):
    follower = User.query.get(id)
    flash('User: %s, has unfollowed you  (%s)'%(follower.name, current_user.name))
    follower.unfollow(current_user)
    #flash('Follower Removed!')
    return redirect('/followers')


@app.route('/follow/<id>', methods=['GET'])
@login_required
def follow(id):
    toFollow = User.query.get(id)
    flash('You are now following %s'%(toFollow.name))
    current_user.follow(toFollow)
    return redirect('/findfollowers')


@app.route('/findfollowers', methods=['GET', 'POST'])
@login_required
def findUsersToFollower():
    # following = current_user.friends
    # notFollowing = []
    # current=0
    # for user in User.query.all():
    #     for friends in current_user.friends:
    #         if user.id == friends.id:
    #             current=1
    #     if current==0:
    #         notFollowing.append(user)
    #     current=0
    notFollowing=current_user.not_following()
    return render_template('findusers.html', title="Find Users", users=notFollowing)
