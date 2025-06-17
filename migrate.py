from db_config import db
from sqlalchemy import text
from app import engine  # Make sure 'engine' is imported from where you define it

# Connect to database and add the column if it doesn't exist
with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE businesses ADD COLUMN phone VARCHAR(20);"))
        print("✅ 'phone' column added successfully to 'businesses' table.")
    except Exception as e:
        print(f"⚠️  Error: {e}")
from db_config import db
from sqlalchemy import text
from app import engine  # Make sure 'engine' is imported from where you define it

# Connect to database and add the column if it doesn't exist
with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE businesses ADD COLUMN phone VARCHAR(20);"))
        print("✅ 'phone' column added successfully to 'businesses' table.")
    except Exception as e:
        print(f"⚠️  Error: {e}")
