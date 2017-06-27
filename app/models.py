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
	equipments = db.relationship('Equipment', backref='owner', lazy='dynamic')


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

	user_id = db.Column (db.Integer, db.ForeignKey('user.id'))

	def __init__(self, name, weight, version_number, brand, model, notes, user_id):
		self.name = name
		self.weight = weight
		self.version_number = version_number
		self.brand = brand
		self.model = model
		self.notes = notes
		self.user_id = user_id

	def __repr__(self):
		return '<Equipment %r>' % (self.name)


class Drone(db.Model):
	__tablename__ = 'drone'

	# unique drone capabilities
	max_payload_cap = db.Column (db.Integer, nullable=False)
	max_speed = db.Column (db.Integer, nullable=False)
	color = db.Column (db.String(20), nullable=False)
	geometry = db.Column (db.String(20), nullable=False) 
	
	equipment_id = db.Column (db.Integer, db.ForeignKey('equipment.id'), primary_key=True)

	def __init__(self, max_payload_cap, max_speed, color, geometry, equipment_id):
		self.max_payload_cap = max_payload_cap
		self.max_speed = max_speed
		self.color = color
		self.geometry = geometry
		self.equipment_id = equipment_id


	def __repr__(self):
		return '<Post %r>' % (self.body)


class Project(db.Model):
	__tablename__ = 'project'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	flights = db.relationship('Flight', backref='project', lazy='dynamic')

	def __init__(self, name, user_id):
		self.name = name
		self.user_id = user_id

class Flight(db.Model):
	__tablename__ = 'flight'
	
	id = db.Column(db.Integer, primary_key =True)
	name = db.Column(db.String(20), nullable = False)

	drone_id = db.Column(db.Integer, db.ForeignKey('drone.equipment_id'))
	project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

	def __init__(self, name, drone_id, project_id):
		self.name = name
		self.drone_id = drone_id
		self.project_id = project_id