from flask_wtf import FlaskForm
from wtforms.fields import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

from app.models import User

# class for sign-up form
class SignUpForm(FlaskForm):
	name = StringField('Name', [DataRequired()])
	email = EmailField('Email', [DataRequired()])
	password = PasswordField('Password', [DataRequired()])
	password_confirm = PasswordField('Confirm Password', [DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

# class for sign-in form
class SignInForm(FlaskForm):
	email = EmailField('Email', [DataRequired()])
	password = PasswordField('Password', [DataRequired()])
	submit = SubmitField('Sign In')

# class for forgot password form
class ForgotForm(FlaskForm):
	email = EmailField('Email', [DataRequired()])
	submit = SubmitField('Send Link')

# class for reset password form
class ResetForm(FlaskForm):
	password = PasswordField('Password', [DataRequired()])
	password_confirm = PasswordField('Confirm Password', [DataRequired(), EqualTo('password')])
	submit = SubmitField('Reset Password')



