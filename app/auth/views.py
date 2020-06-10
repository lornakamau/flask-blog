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
    categories = Category.query.all()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        mail_message("Welcome to Pitch","email/welcome_user",user.email,user=user)

        return redirect(url_for('auth.login'))
    title = "New Account | Pitch"
    return render_template('auth/signup.html', signup_form = form, title=title)