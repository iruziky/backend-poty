#!/bin/sh
set -e
alembic upgrade head

if [ "$RUN_RESET_DB" = "true" ]; then
  echo "Rodando script de limpeza do banco..."
  python scripts/reset_db.py
fi

exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
