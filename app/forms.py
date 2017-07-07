from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, BooleanField, IntegerField, PasswordField, SelectField,  TextAreaField, DecimalField	
from wtforms.validators import DataRequired, Optional, ValidationError
# from wtforms.fields.html5 import DateField 
from wtforms_components import DateField, TimeField


def is_positive(FlaskForm, field):
	if field.data < 0:
		raise ValidationError(field.field_name+' must be positive.')

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
	date = DateField('date', format='%Y-%m-%d', validators=[Optional()])
	duration_hours = IntegerField('duration_hours', validators=[is_positive])
	duration_mins = IntegerField('duration_mins', validators=[is_positive])
	duration_secs = IntegerField('duration_secs', validators=[is_positive])
	flight_types=[
		('Commercial','Commercial'), 
		('Emergency','Emergency'), 
		('Hobby','Hobby'), 
		('Maintenance','Maintenance'), 
		('Science','Science'), 
		('Simulator','Simulator'), 
		('Test Flight','Test Flight'), 
		('Training Flight','Training Flight')
	]
	flight_type = SelectField('flight_type', choices=flight_types, validators=[DataRequired()])
	more_type_info = StringField('more_type_info', validators=[Optional()])
	operation_types=[
		('VLOS','VLOS'),
		('EVLOS','EVLOS'),
		('BVLOS/BLOS', 'BVLOS/BLOS'),
		('Autonomous', 'Autonomous'),
		('FPV','FPV')
	]
	operation_type= SelectField('operation_type', choices=operation_types, validators=[DataRequired()])

	project = SelectField('project', coerce=int, validators=[DataRequired()])

	drone = SelectField('drone', coerce=int,validators=[DataRequired()])


	night_flight = BooleanField('night_flight', validators=[DataRequired()])
	landing_count = IntegerField('landing_count', validators=[DataRequired()])
	travelled_distance = DecimalField('travelled_distance', validators=[DataRequired()])
	max_agl_altitude = DecimalField('max_agl_altitude', validators=[DataRequired()])
	notes = TextAreaField('notes', validators=[Optional()])
	weather_description = TextAreaField('weather_description', validators=[Optional()])

class LogForm(FlaskForm):
	log_file = FileField('log_file', validators=[FileRequired()])