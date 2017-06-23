from app import db


db.engine.execute("CREATE DATABASE IF NOT EXISTS airborne;")
db.engine.execute("USE airborne;")

db.create_all()

