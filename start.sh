#!/bin/sh
set -e

echo "[start] Waiting for database..."
RETRIES=40
SLEEP=1

while true; do
  if python - <<'PYCODE'
import os, sqlalchemy as sa
url = os.getenv('DB_URL')
if not url:
    raise SystemExit(1)
engine = sa.create_engine(url)
with engine.connect() as conn:
    conn.execute(sa.text('SELECT 1'))
PYCODE
  then
    echo "[start] Database reachable."; break
  fi
  RETRIES=$((RETRIES-1))
  if [ $RETRIES -le 0 ]; then
    echo "[start] Database not reachable after retries." >&2
    exit 1
  fi
  echo "[start] DB not ready; retrying... ($RETRIES left)"
  sleep $SLEEP
done

echo "[start] Running migrations..."
alembic upgrade head || { echo "[start] Migration failed" >&2; exit 1; }

echo "[start] Seeding categories (idempotent)..."
python - <<'PYCODE'
from app.db.connection import SessionLocal
from app.db.seed import seed_initial_categories

session = SessionLocal()
try:
    seed_initial_categories(session)
finally:
    session.close()
PYCODE

echo "[start] Launching Uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
