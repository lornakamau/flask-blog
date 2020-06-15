from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,ValidationError,BooleanField,TextAreaField
from wtforms.validators import Required,Email,EqualTo,Length
from ..models import User
from email_validator import validate_email, EmailNotValidError

class SignUpForm(FlaskForm):
    email = StringField('Email Address',validators=[Required(),Email()])
    username = StringField('Username',validators = [Required(),Length(min=2,max=20)])
    bio = TextAreaField("Give a short decription of yourself", validators=[Required()])
    password = PasswordField('Password',validators = [Required()])
    password_confirm = PasswordField('Confirm Password',validators = [Required(), EqualTo('password',message = 'Passwords must match')])
    submit = SubmitField('Sign Up')

    def validate_email(self,data_field):
            if User.query.filter_by(email =data_field.data).first():
                raise ValidationError('There is an account with that email')

    def validate_username(self,data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('That username is taken')

class LoginForm(FlaskForm):
    email = StringField('Your Email Address',validators=[Required(),Email()])
    password = PasswordField('Password',validators =[Required()])
    remember = BooleanField('Remember Me') #confirms if user wants to be logged out after session
    submit = SubmitField('Sign In')
