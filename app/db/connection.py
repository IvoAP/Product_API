import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

DB_URL = os.getenv("DB_URL")
if not DB_URL:
	raise RuntimeError("Environment variable DB_URL is not defined. Ensure the .env file is loaded or export DB_URL.")
engine = create_engine(DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator:
	"""FastAPI dependency that yields a DB session per request.

	Example:
		@app.get("/items")
		def list_items(db: Session = Depends(get_db)):
			...

	The session is closed automatically after the request lifecycle.
	"""
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
