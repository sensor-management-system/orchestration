#!/bin/sh

echo "[LOG] Using database: $1"
echo "[LOG] Running migrations"
python manage.py db upgrade
echo "[LOG] Starting gunicorn on port $2"
gunicorn -b 0.0.0.0:5000 manage:app --reload