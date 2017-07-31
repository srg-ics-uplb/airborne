#!/bin/bash
set -e 

if [ ! -e flask ]
then
echo "Creating virtual environment..."
virtualenv flask
fi

echo "Installing required Flask extensions..."
flask/Scripts/pip install flask
flask/Scripts/pip install flask-login
flask/Scripts/pip install flask-bcrypt
flask/Scripts/pip install flask-sqlalchemy
flask/Scripts/pip install mysql-python
flask/Scripts/pip install flask-wtf
flask/Scripts/pip install wtforms-components
flask/Scripts/pip install flask-migrate
flask/Scripts/pip install pymavlink
flask/Scripts/pip install flask-googlemaps

export FLASK_APP=app/__init__.py

if [ ! -e migrations ]
then
echo "No migrations folder yet."
echo "Initializing migration folder..."
flask/Scripts/flask db init

mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS airborne;"
flask/Scripts/flask db migrate
flask/Scripts/flask db upgrade
echo "Apply workaround for storing large dronekit-la outputs in db"
mysql -u root -p -e "ALTER TABLE log MODIFY content LONGTEXT;"
fi

