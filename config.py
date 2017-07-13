WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = 'root'

GPS_COORDINATE_FILES_FOLDER = 'app\uploads\gps'
UPLOAD_FOLDER = 'app\uploads\logs'
ALLOWED_EXTENSIONS = ['bin', 'log', 'tlog']
MAX_CONTENT_LENGTH = 30 * 1024 * 1024


#some constants set to avoid vehicle definition fail
DRONE_TYPE = 'copter '
DRONE_TYPE_ARG = ' -m ' + DRONE_TYPE
FRAME_TYPE = 'QUAD '
FRAME_TYPE_ARG = ' -f ' + FRAME_TYPE

#log analyzer set to output json format
LOG_ANALYZER_DIR = 'dronekit-la\dronekit-la.exe -s json ' + DRONE_TYPE_ARG + FRAME_TYPE_ARG

SQLALCHEMY_DATABASE_URI = 'mysql://' + MYSQL_USERNAME + ':' + MYSQL_PASSWORD + '@localhost/airborne'
SQLALCHEMY_TRACK_MODIFICATIONS = False