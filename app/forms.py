from flask_wtf import Form
from wtforms import StringField, BooleanField, IntegerField, PasswordField, SelectField
from wtforms.validators import DataRequired

class LoginForm(Form):

	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)

class SignupForm(Form):
	firstname = StringField('firstname', validators=[DataRequired()])
	middlename = StringField('middlename', validators=[DataRequired()])
	lastname = StringField('lastname', validators=[DataRequired()])
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	email = StringField('email', validators=[DataRequired()])
	age = IntegerField('age', validators=[DataRequired()])
	sex = SelectField('sex', choices=[('m', 'Male'), ('f','Female')])