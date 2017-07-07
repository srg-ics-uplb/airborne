from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt



app = Flask(__name__)
app.config.from_object('config')



db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

# blueprints
from .views.general import general
app.register_blueprint(general)

from .views.user import user
app.register_blueprint(user)

from .views.error import error
app.register_blueprint(error)

from .views.flight import flight
app.register_blueprint(flight)

from .views.project import project
app.register_blueprint(project)

from .views.drone import drone
app.register_blueprint(drone)

from .views.log import log
app.register_blueprint(log)


