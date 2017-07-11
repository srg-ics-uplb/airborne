WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = 'root'

UPLOAD_FOLDER = 'app\uploads\logs'
ALLOWED_EXTENSIONS = set(['bin'])

#log analyzer set to output json format
LOG_ANALYZER_DIR = 'dronekit-la\dronekit-la.exe -s json '


SQLALCHEMY_DATABASE_URI = 'mysql://' + MYSQL_USERNAME + ':' + MYSQL_PASSWORD + '@localhost/airborne'
SQLALCHEMY_TRACK_MODIFICATIONS = False