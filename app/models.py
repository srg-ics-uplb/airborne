from app import db

class User(db.Model):
	__tablename__ = 'user'
	id = db.Column (db.Integer, primary_key=True)
	first_name = db.Column(db.String(64), index=True)
	middle_name = db.Column(db.String(64), index=True)
	last_name = db.Column(db.String(64), index=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email= db.Column(db.String(120), index=True, unique=True)
	password = db.Column(db.String(256), index=True)
	age = db.Column(db.Integer, index=True)
	sex = db.Column(db.String(1), index=True)
	authenticated = db.Column(db.Boolean, default=False)
	posts = db.relationship('Post', backref='author', lazy='dynamic')



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
	name = db.Column (db.String(140), index=True, unique=True)
	weight = db.Column (db.Integer, index=True)
	version_number = db.Column(db.String(20), index=True)
	brand = db.Column (db.String(20), index=True)
	model = db.Column (db.String(20), index=True)
	notes = db.column (db.Text, index=True)

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
	max_payload_cap = db.Column (db.Integer, index=True)
	max_speed = db.Column (db.Integer, index=True)
	color = db.Column (db.String(20), index=True)
	geometry = db.Column (db.String(20), index=True) 
	
	equipment_id = db.Column (db.Integer, db.ForeignKey('equipment.id'))

	def __init__(self, max_payload_cap, max_speed, color, geometry):
		self.max_payload_cap = max_payload_cap
		self.max_speed = max_speed
		self.color = color
		self.geometry = geometry

		
	def __repr__(self):
		return '<Post %r>' % (self.body)


