WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = 'root'

UPLOAD_FOLDER = 'app\\uploads\\logs'
ALLOWED_EXTENSIONS = set(['bin'])

SQLALCHEMY_DATABASE_URI = 'mysql://' + MYSQL_USERNAME + ':' + MYSQL_PASSWORD + '@localhost/airborne'
SQLALCHEMY_TRACK_MODIFICATIONS = False