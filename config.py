WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = 'root'


UPLOAD_FOLDER = 'app\uploads\logs'
ALLOWED_EXTENSIONS = ['bin', 'log', 'tlog']
MAX_CONTENT_LENGTH = 30 * 1024 * 1024

GPS_COORDINATE_FILE_FOLDER = UPLOAD_FOLDER + '\gps'
PROCESSED_OUTPUT_FILE_FOLDER = UPLOAD_FOLDER + '\processed_la'
ORIGINAL_LOG_FILE_FOLDER = UPLOAD_FOLDER + '\original'

#some constants set to avoid vehicle definition fail
DRONE_TYPE = 'copter '
DRONE_TYPE_ARG = ' -m ' + DRONE_TYPE
FRAME_TYPE = 'QUAD '
FRAME_TYPE_ARG = ' -f ' + FRAME_TYPE

#log analyzer set to output json format
LOG_ANALYZER_DIR = 'dronekit-la\dronekit-la.exe -s json ' + DRONE_TYPE_ARG + FRAME_TYPE_ARG

SQLALCHEMY_DATABASE_URI = 'mysql://' + MYSQL_USERNAME + ':' + MYSQL_PASSWORD + '@localhost/airborne'
SQLALCHEMY_TRACK_MODIFICATIONS = False