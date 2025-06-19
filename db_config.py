from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
import os

# ✅ Load environment variables
load_dotenv()

SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")

if not SUPABASE_DB_URL:
    raise ValueError("SUPABASE_DB_URL not found in .env")

engine = create_engine(SUPABASE_DB_URL)
Session = scoped_session(sessionmaker(bind=engine))
session = Session()
