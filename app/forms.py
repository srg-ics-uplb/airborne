from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, PasswordField, SelectField,  TextAreaField, DecimalField
from wtforms.validators import DataRequired, Optional

class LoginForm(FlaskForm):

	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)

class SignupForm(FlaskForm):
	firstname = StringField('firstname', validators=[DataRequired()])
	middlename = StringField('middlename', validators=[DataRequired()])
	lastname = StringField('lastname', validators=[DataRequired()])
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	email = StringField('email', validators=[DataRequired()])
	age = IntegerField('age', validators=[DataRequired()])
	sex = SelectField('sex', choices=[('m', 'Male'), ('f','Female')])


class DroneForm(FlaskForm):
	name = StringField('name', validators=[DataRequired()])
	weight = DecimalField('weight', validators=[DataRequired()])
	version_number = StringField('version_num', validators=[DataRequired()])
	brand = StringField('brand', validators=[DataRequired()])
	model = StringField('model', validators=[DataRequired()])
	notes = TextAreaField('notes', validators=[Optional()])
	max_payload_cap = DecimalField('max_payload_cap', validators=[DataRequired()])
	max_speed = DecimalField('max_speed', validators=[DataRequired()])
