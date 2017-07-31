"""Config file for Airborne"""

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'


#Database Constants
DB_TYPE = 'mysql://'
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_ROUTE = '@localhost/'

SQLALCHEMY_DATABASE_URI = DB_TYPE + MYSQL_USERNAME + ':' + MYSQL_PASSWORD + MYSQL_ROUTE + 'airborne'
SQLALCHEMY_TRACK_MODIFICATIONS = False

#enable auto template reload
TEMPLATES_AUTO_RELOAD = True


#for Google Maps API
GOOGLEMAPS_KEY = 'AIzaSyBnNjcDq_RASeUwI3HHYljhBht7CtjGYx0'

#Upload restraints
ALLOWED_EXTENSIONS = ['bin', 'log', 'tlog']
MAX_CONTENT_LENGTH = 30 * 1024 * 1024


#Directories for uploaded content
UPLOAD_FOLDER = 'app\\uploads\\logs'
GPS_COORDINATE_FILE_FOLDER = UPLOAD_FOLDER + '\\gps'
PROCESSED_OUTPUT_FILE_FOLDER = UPLOAD_FOLDER + '\\processed_la'
ORIGINAL_LOG_FILE_FOLDER = UPLOAD_FOLDER + '\\original'

#some constants set to avoid vehicle definition fail
DRONE_TYPE = 'copter '
DRONE_TYPE_ARG = ' -m ' + DRONE_TYPE
FRAME_TYPE = 'QUAD '
FRAME_TYPE_ARG = ' -f ' + FRAME_TYPE


### THESE ARGS ARE MADE FOR USE ON WINDOWS SYSTEMS

#for use with mavlogdump
PYTHON_DIR = 'flask\\Scripts\\python.exe '

#log analyzer set to output json format
LOG_ANALYZER_DIR = 'tools\\dronekit-la\\dronekit-la.exe -s json ' + DRONE_TYPE_ARG + FRAME_TYPE_ARG

#log analyzer set to output plaintext format
LOG_ANALYZER_TXT_DIR = 'tools\\dronekit-la\\dronekit-la.exe -s plain-text ' + DRONE_TYPE_ARG + FRAME_TYPE_ARG

#mavlogdump for parsing a csv file containing gps-related data from bin logs
MAVLOGDUMP_ARGS = '--format csv --types GPS '
MAVLOGDUMP_DIR = 'tools\\mavlogdump.py ' + MAVLOGDUMP_ARGS
MAVLOGDUMP_RUN = PYTHON_DIR + MAVLOGDUMP_DIR + ORIGINAL_LOG_FILE_FOLDER


### THESE ARGS ARE MADE FOR USE ON LINUX SYSTEMS

#for use with mavlogdump
PYTHON_DIR_2 = 'flask\\Scripts\\python '

#log analyzer set to output json format
LOG_ANALYZER_DIR_2 = 'dronekit-la -s json ' + DRONE_TYPE_ARG + FRAME_TYPE_ARG

#log analyzer set to output plaintext format
LOG_ANALYZER_TXT_DIR_2 = 'dronekit-la -s plain-text ' + DRONE_TYPE_ARG + FRAME_TYPE_ARG

#mavlogdump for parsing a csv file containing gps-related data from bin logs
MAVLOGDUMP_ARGS_2 = '--format csv --types GPS '
MAVLOGDUMP_DIR_2 = 'tools\\mavlogdump.py ' + MAVLOGDUMP_ARGS_2
MAVLOGDUMP_RUN_2 = PYTHON_DIR_2 + MAVLOGDUMP_DIR_2 + ORIGINAL_LOG_FILE_FOLDER


