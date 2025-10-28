import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

DB_URL = os.getenv("DB_URL")
if not DB_URL:
	raise RuntimeError("Variável de ambiente DB_URL não definida. Certifique-se de que o .env foi carregado ou exporte DB_URL.")
engine = create_engine(DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator:
	"""Dependency para FastAPI que fornece uma sessão de banco por requisição.

	Uso:
		@app.get("/items")
		def list_items(db: Session = Depends(get_db)):
			...
	A sessão é fechada automaticamente ao final da requisição.
	"""
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
