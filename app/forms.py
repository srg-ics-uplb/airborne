from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, BooleanField, IntegerField, PasswordField, SelectField,  TextAreaField, DecimalField	
from wtforms.validators import DataRequired, InputRequired, Optional, ValidationError, NumberRange, Email,EqualTo, Length
# from wtforms.fields.html5 import DateField 
from wtforms_components import DateField, TimeField
from app import app


def is_positive(FlaskForm, field):
	if field.data < 0:
		raise ValidationError(field.name+' must be positive.')

class LoginForm(FlaskForm):

	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)

class SignupForm(FlaskForm):
	firstname = StringField('firstname', validators=[InputRequired(), Length(max=64)])
	middlename = StringField('middlename', validators=[InputRequired(), Length(max=64)])
	lastname = StringField('lastname', validators=[InputRequired(),Length(max=64)])
	username = StringField('username', validators=[InputRequired(),Length(min=8, max=64)])
	password = PasswordField('password', validators=[InputRequired(),EqualTo('confirm_password', message='Passwords do not match!'), Length(min=8, max=32)])
	confirm_password = PasswordField('confirm_password')
	email = StringField('email', validators=[Email(), Length(max=120)])
	age = IntegerField('age', validators=[NumberRange(min=18)])
	sex = SelectField('sex', choices=[('m', 'Male'), ('f','Female')])


class DroneForm(FlaskForm):
	name = StringField('name', validators=[InputRequired(), Length(min=5, max=20)])
	weight = DecimalField('weight', validators=[InputRequired(), NumberRange(min=0)])
	version_number = StringField('version_num', validators=[InputRequired(), Length(max=20)])
	brand = StringField('brand', validators=[InputRequired(), Length(min=5, max=20)])
	model = StringField('model', validators=[InputRequired(), Length(min=5, max=20)])
	notes = TextAreaField('notes', validators=[Optional()])
	max_payload_cap = DecimalField('max_payload_cap', validators=[InputRequired(), NumberRange(min=0)])
	max_speed = DecimalField('max_speed', validators=[InputRequired(), NumberRange(min=0)])

class ProjectForm(FlaskForm):
	name = StringField('name', validators=[DataRequired()])
	description = TextAreaField('notes', validators=[Optional()])

class FlightForm(FlaskForm):
	name = StringField('name', validators=[DataRequired()])
	location = StringField('location', validators=[DataRequired()])
	date = DateField('date', format='%Y-%m-%d', validators=[Optional()])
	duration_hours = IntegerField('duration_hours', validators=[NumberRange(min=0, max=23)])
	duration_mins = IntegerField('duration_mins', validators=[NumberRange(min=0, max=59)])
	duration_secs = IntegerField('duration_secs', validators=[NumberRange(min=0, max=59)])
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


	night_flight = BooleanField('night_flight', validators=[Optional()])
	landing_count = IntegerField('landing_count', validators=[DataRequired()])
	travelled_distance = DecimalField('travelled_distance', validators=[DataRequired()])
	max_agl_altitude = DecimalField('max_agl_altitude', validators=[DataRequired()])
	notes = TextAreaField('notes', validators=[Optional()])
	weather_description = TextAreaField('weather_description', validators=[Optional()])

class LogForm(FlaskForm):
	log_file = FileField('log_file', validators=[FileRequired(), FileAllowed(app.config['ALLOWED_EXTENSIONS'], 'Should be a dataflash text dump(*.log), telemetry log(*.tlog), or dataflash binary log(*.bin)')])