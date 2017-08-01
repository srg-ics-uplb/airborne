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
		mysqlclient (might require some manual installation) or mysql-python
		Flask-WTForms
		WTForms-Components
		Flask-Migrate
		Pymavlink
		Flask-GoogleMaps
		virtualenv

Setup:
======

Install the latest version of Python 2.7 and MySQL. Also install the required connectors for MySQL.
On Windows, you can download them here: [Python](https://www.python.org/downloads/windows/) [MySQL](https://dev.mysql.com/downloads/mysql/)

On Linux, you can use the following commands:

	sudo apt-get update
	sudo apt-get install mysql-server
	sudo apt-get install python2.7 libmysqlclient-dev python-mysqldb

Clone the github repository. 

	git clone https://github.com/ClarkAlmazan/airborne
Install virtualenv.

	pip install virtualenv

Navigate to the cloned repo.

	cd airborne

Open config.py and set your MySQL credentials on constants `MYSQL_USERNAME` and `MYSQL_PASSWORD`. Set the address of the database server on `MYSQL_ROUTE`.

	MYSQL_USERNAME = <some special user>
	MYSQL_PASSWORD = <some special password>
	MYSQL_ROUTE = <@address:port>
Get your own API key from Google Maps from [here](https://developers.google.com/maps/documentation/javascript/get-api-key)

Also on config.py, set your api key on constant 'GOOGLEMAPS_KEY'

	GOOGLEMAPS_KEY = <your api key>
Run the install script. It will install most of the components required. This requires Bash. Grant permissions if necessary.

	chmod +x install.sh
	./install.sh
Download a copy of dronekit-la from [here](https://github.com/dronekit/dronekit-la/releases/latest). 
On Windows, place the contents of the zip file inside the tools folder. You'll have something that looks like this:

	|
	| app
	| flask
	| ...
	| tools
	|--- dronekit-la
	|---|--- dronekit-la.exe
	|---|--- LICENSE
	|---|--- README.md
	|--- mavlogdump.py

On Linux, install it using the commands below:

	wget https://github.com/dronekit/dronekit-la/releases/download/v0.5/dronekit-la_0.5_amd64.deb
	sudo dpkg -i dronekit-la_0.5_amd64.deb
	sudo apt-get install -f

For production purposes, install Gunicorn (Linux only):

	pip install gunicorn

How to Run:
=====

To run the development server(Windows and Linux), use:

	flask/Scripts/python run.py #for Windows
	flask/bin/python run.py #for Linux
To run the production server (Linux only), use:
	
	chmod +x production-linux.sh #only if necessary
	./production-linux.sh

