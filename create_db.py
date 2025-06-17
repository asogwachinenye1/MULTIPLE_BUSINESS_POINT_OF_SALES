from db_config import app, db
from models import *

with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully.")
