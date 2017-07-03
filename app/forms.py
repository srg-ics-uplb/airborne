from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, PasswordField, SelectField,  TextAreaField, DecimalField, DateField
from wtforms.validators import DataRequired, Optional
from wtforms_components import TimeField

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

class ProjectForm(FlaskForm):
	name = StringField('name', validators=[DataRequired()])
	description = TextAreaField('notes', validators=[Optional()])

class FlightForm(FlaskForm):
	name = StringField('name', validators=[DataRequired()])
	location = StringField('location', validators=[DataRequired()])
	date = DateField('date', validators=[DataRequired()])
	duration = TimeField('duration', validators=[DataRequired()])
	flight_type = SelectField('flight_type', choices=['Commercial', 'Emergency', 'Hobby', 'Maintenance', 'Science', 'Simulator', 'Test Flight', 'Training Flight'], validators=[DataRequired()])
	night_flight = BooleanField('night_flight', validators=[DataRequired()])
	landing_count = IntegerField('landing_count', validators=[DataRequired()])
	travelled_distance = DecimalField('travelled_distance', validators=[DataRequired()])
	max_agl_altitude = DecimalField('max_agl_altitude', validators=[DataRequired()])
	notes = TextAreaField('notes', validators=[Optional()])
	weather_description = TextAreaField('weather_description', validators=[Optional()])