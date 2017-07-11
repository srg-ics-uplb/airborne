from app import db

class User(db.Model):
	__tablename__ = 'user'
	id = db.Column (db.Integer, primary_key=True)
	first_name = db.Column(db.String(64), nullable=False)
	middle_name = db.Column(db.String(64), nullable=False)
	last_name = db.Column(db.String(64), nullable=False)
	username = db.Column(db.String(64), nullable=False, unique=True)
	email= db.Column(db.String(120), nullable=False, unique=True)
	password = db.Column(db.String(256), nullable=False)
	age = db.Column(db.Integer, nullable=False)
	sex = db.Column(db.String(1), nullable=False)
	authenticated = db.Column(db.Boolean, default=False)
	# equipments = db.relationship('Equipment', backref='owner', lazy='dynamic')
	projects = db.relationship('Project', backref='owner', lazy='dynamic')
	drones = db.relationship('Drone', backref='owner', lazy='dynamic')

	def __init__(self, first_name, middle_name, last_name, email, username, password, age, sex):
		self.first_name = first_name
		self.last_name = last_name
		self.middle_name = middle_name
		self.email = email
		self.password = password
		self.age = age
		self.username = username
		self.sex = sex

	def __repr__(self):
		return '<User %r>' % (self.first_name+' '+self.middle_name+' '+self.last_name)

	def get_id(self):
		try:
			return unicode(self.id)
		except NameError:
			return str(self.id)

	@property
	def is_authenticated(self):
		return self.authenticated

	@property
	def is_active(self):
		return True
	
	@property
	def is_anonymous(self):
		return False		
	
# base equipment entity
# where drones, cameras, batteries, and other future equipment to implement are derived
class Equipment(db.Model):
	__tablename__ = 'equipment'
	id = db.Column (db.Integer, primary_key=True)
	name = db.Column (db.String(140), nullable=False, unique=True)
	weight = db.Column (db.Integer, nullable=False)
	version_number = db.Column(db.String(20), nullable=False)
	brand = db.Column (db.String(20), nullable=False)
	model = db.Column (db.String(20), nullable=False)
	notes = db.Column (db.Text)
	equipment_type = db.Column(db.String(5), nullable=False)

	user_id = db.Column (db.Integer, db.ForeignKey('user.id'))

	
	__mapper_args__ = {
		'polymorphic_on': equipment_type,
		'polymorphic_identity': 'equipment'
	}
	
	def __init__(self, name, weight, version_number, brand, model, notes, equipment_type, user_id):
		self.name = name
		self.weight = weight
		self.version_number = version_number
		self.brand = brand
		self.model = model
		self.notes = notes
		self.equipment_type = equipment_type
		self.user_id = user_id
	

	def __repr__(self):
		return '<Equipment %r>' % (self.name)
	def get_id(self):
		return unicode(self.id)

	

class Drone(Equipment):
	__tablename__ = 'drone'

	# unique drone capabilities
	id = db.Column (db.Integer, db.ForeignKey('equipment.id'), primary_key=True)
	max_payload_cap = db.Column (db.Integer, nullable=False)
	max_speed = db.Column (db.Integer, nullable=False)
	# color = db.Column (db.String(20), nullable=False)
	# geometry = db.Column (db.String(20), nullable=False) 
	
	flights = db.relationship('Flight', backref='equipment', lazy='dynamic')

	__mapper_args__ = {
		'polymorphic_identity': 'drone',
		'inherit_condition': (id==Equipment.id)
	}

	def __init__(self, name, weight, version_number, brand, model, notes, equipment_type, user_id, max_payload_cap, max_speed):
		super(Drone, self).__init__(name, weight, version_number, brand, model, notes, equipment_type, user_id)
		self.max_payload_cap = max_payload_cap
		self.max_speed = max_speed
		# self.color = color
		# self.geometry = geometry
	


	def __repr__(self):
		return '<Drone (name=%s, weight=%s, version_number=%s, brand=%s, model=%s, max_payload_cap=%s, max_speed=%s)>' % (self.name, self.weight, self.version_number, self.brand, self.model, self.max_payload_cap, self.max_speed)


class Project(db.Model):
	__tablename__ = 'project'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	description = db.Column(db.Text)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	flights = db.relationship('Flight', backref='project', lazy='dynamic')

	def __init__(self, name, description,user_id):
		self.name = name
		self.description = description
		self.user_id = user_id


class Flight(db.Model):
	__tablename__ = 'flight'
	
	id = db.Column(db.Integer, primary_key =True)
	name = db.Column(db.String(20), nullable = False)
	location = db.Column(db.String(255), nullable = False)
	date = db.Column(db.Date, nullable = False)
	duration = db.Column(db.Integer, nullable = False)
	flight_type = db.Column(db.String(20))
	more_type_info = db.Column(db.String(20))
	operation_type = db.Column(db.String(20))
	night_flight = db.Column(db.Boolean, nullable = False)
	landing_count = db.Column(db.Integer, nullable = False, default=0)
	travelled_distance = db.Column(db.Float, nullable = False)
	max_agl_altitude = db.Column(db.Float, nullable = False)
	notes = db.Column(db.Text)

	#Weather conditions data
	#For now, only textual description is used
	# cloud_cover = db.Column(db.Float, nullable = False)
	# temperature = db.Column(db.Float, nullable = False)
	# wind_speed = db.Column(db.Float, nullable = False)
	# humidity = db.Column(db.Float, nullable = False)
	weather_description = db.Column(db.Text)

	#Reference to drone used during flight and project
	drone_id = db.Column(db.Integer, db.ForeignKey('drone.id'))
	project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

	#Log files
	logs = db.relationship('Log', backref="flight", lazy='dynamic')

	def __init__(self, name, location, date, duration, flight_type, more_type_info, operation_type, night_flight, landing_count, travelled_distance, max_agl_altitude, notes, weather_description, drone_id, project_id):
		self.name = name
		self.location = location
		self.date = date
		self.duration = duration
		self.flight_type = flight_type
		self.more_type_info = more_type_info
		self.operation_type = operation_type
		self.night_flight = night_flight
		self.landing_count = landing_count
		self.travelled_distance = travelled_distance
		self.max_agl_altitude = max_agl_altitude
		self.notes = notes
		self.weather_description = weather_description
		self.drone_id = drone_id
		self.project_id = project_id

class Log(db.Model):
	__tablename__ = 'log'

	id = db.Column(db.Integer, primary_key=True)
	filename = db.Column(db.String(255), nullable=False)
	content = db.Column(db.Text)
	flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'))

	def __init__(self, filename, content,  flight_id):
		self.filename = filename
		self.content = content
		self.flight_id = flight_id