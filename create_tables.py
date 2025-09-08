from app import app, db
from models import StudentBody, BodyEvent  # Import your new models

with app.app_context():
    # This will create tables for any models that do not exist yet.
    # It will NOT modify existing tables.
    db.create_all()
    print("Database tables created/updated (if they didn't exist).")