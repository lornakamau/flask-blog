from flask import render_template, redirect, url_for, flash, request
from . import auth
from ..models import User
from .forms import SignUpForm, LoginForm
from .. import db
from flask_login import login_user, logout_user, login_required
from ..email import mail_message

# app.config['SECRET_KEY'] =''
@auth.route('/signup', methods = ["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit() and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path=f'photos/{filename}'
        user = User(email = form.email.data, username = form.username.data, password = form.password.data, bio=form.bio.data, profile_pic_path=path)
        db.session.add(user)
        db.session.commit()
        mail_message("Welcome to SoftBlog","email/welcome_user",user.email,user=user)

        return redirect(url_for('auth.login'))
    title = "New Account | SoftBlog"
    return render_template('auth/signup.html', signup_form = form, title=title)

@auth.route('/login', methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember.data)
            return redirect(request.args.get('next') or url_for('main.posts'))
        flash('Invalid username or password', 'danger')
    
    title = "Login | SoftBlog"
    return render_template('auth/login.html', login_form = form, title=title)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.posts"))