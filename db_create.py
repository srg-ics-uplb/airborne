from app import db

db.engine.execute("USE airborne;")

db.create_all()

