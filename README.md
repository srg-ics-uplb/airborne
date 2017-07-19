# Airborne
Drone flight management and log analytics

Prerequisites:
======
	MySQL 5.7	
	Python 2.7
	Flask 0.12
	dronekit-la
	mavlogdump.py(from Pymavlink tools repo)	
	The following Python/Flask extensions:		
		Flask-Login
		Flask-Bcrypt
		Flask-SQLAlchemy	
		Flask-mysqlclient (might require some manual installation)
		Flask-WTForms
		Flask-Migrate
		Pymavlink
		Flask-GoogleMaps
		virtualenv

Setup:
======
Clone the github repository. 

	git clone https://github.com/ClarkAlmazan/airborne
Install virtualenv.

	pip install virtualenv
Inside the newly cloned repository, create a new virtual environment.

	cd airborne
	virtualenv flask

If you're on Windows, activate the virtual environment using this:

	flask/Scripts/activate.bat
If you're on Linux, use this instead:
	
	./flask/bin/activate.sh

Create a new folder called 'tools'.

	mkdir tools
Download a copy of dronekit-la that's appropriate for your OS from [here](https://github.com/dronekit/dronekit-la/releases/latest) as well as mavlogdump.py from the Pymavlink repo's [tools](https://github.com/ArduPilot/pymavlink/blob/master/tools/mavlogdump.py) folder.

Install the remaining dependencies using pip:

	pip install flask
	pip install flask-login
	pip install flask-bcrypt
	pip install flask-sqlalchemy
	pip install flask-wtforms
	pip install flask-migrate
	pip install pymavlink
	pip install flask-googlemaps

To run the development server, use:

	python run.py
Currently there is no available server for production use. It'll be there soon.

