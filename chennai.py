
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text

load_dotenv()  # or load_dotenv('/absolute/path/to/.env')

db_url = os.getenv("DB_URL")
if not db_url:
    raise RuntimeError("DB_URL is missing. Check .env or shell export.")

engine = create_engine(db_url, future=True, pool_pre_ping=True)

with engine.connect() as conn:
    print(conn.execute(text("SELECT current_user, current_database(), version()")).all())
