# Airborne
Drone flight management and log analytics web application built using Python/Flask, MySQL, and Bootstrap.
Log analysis is done using [dronekit-la](la.dronekit.io).

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
I don't have an install script ready yet. So bear with the manual installation process for now.


Install the latest version of Python 2.7 and MySQL.
On Windows, you can download them here: [Python](https://www.python.org/downloads/windows/) [MySQL](https://dev.mysql.com/downloads/mysql/)

On Linux, you can use the following commands:

	sudo apt-get update
	sudo apt-get install mysql-server
	sudo apt-get install python2.7

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

Set the FLASK_APP environment variable to app/__init__.py

	export FLASK_APP=app/__init__.py

Create a new database in MySQL for Airborne. You can also create your own user that Airborne will use to access your database.
	
	create database airborne
Open config.py and set your MySQL credentials on constants `MYSQL_USERNAME` and `MYSQL_PASSWORD`

	MYSQL_USERNAME = <some special user>
	MYSQL_PASSWORD = <some special password>
Get your own API key from Google Maps from [here](https://developers.google.com/maps/documentation/javascript/get-api-key) and create a new file called `api_key.py`. Inside the file, create a variable named `api_key` and set your API key to it. Here's a sample of the file.

	"""
	api_key.py
	Python module that stores the Google Maps API Key
	You can get your own from here: https://developers.google.com/maps/documentation/javascript/get-api-key
	"""
	api_key = <your api key>

Run the initial migration

	flask db init
	flask db migrate
	flask db upgrade



To run the development server, use:

	python run.py
Currently there is no available server for production use. It'll be there soon.

