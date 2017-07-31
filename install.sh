#!/bin/bash
set -e 

if [ ! -e flask ]
then
echo "Creating virtual environment..."
virtualenv flask
fi

echo "Installing required Flask extensions..."
flask/bin/pip install flask
flask/bin/pip install flask-login
flask/bin/pip install flask-bcrypt
flask/bin/pip install flask-sqlalchemy
flask/bin/pip install mysql-python
flask/bin/pip install flask-wtf
flask/bin/pip install wtforms-components
flask/bin/pip install flask-migrate
flask/bin/pip install pymavlink
flask/bin/pip install flask-googlemaps

export FLASK_APP=app/__init__.py

if [ ! -e migrations ]
then
echo "No migrations folder yet."
echo "Initializing migration folder..."
flask/bin/flask db init

mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS airborne;"
flask/bin/flask db migrate
flask/bin/flask db upgrade
echo "Apply workaround for storing large dronekit-la outputs in db"
mysql -u root -p -e "ALTER TABLE log MODIFY content LONGTEXT;"
fi

