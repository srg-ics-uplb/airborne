#!flask/Scripts/python
from app import app

if __name__ == "__main__":
	app.jinja_env.cache = {}
	app.run(host='0.0.0.0', debug=True, threaded=True)