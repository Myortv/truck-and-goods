#!/usr/bin/env bash
set -e

echo "Loading Database..."
python app/db/preload_database.py


echo "Starting Uvicorn server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
