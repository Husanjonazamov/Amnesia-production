#!/bin/bash

# Postgres tayyor bo'lishini kutish
while ! nc -z db 5432; do
  sleep 2
  echo "Waiting for Postgres..."
done

# Django static fayllarni to'plash
echo "📦 Collectstatic"
python3 manage.py collectstatic --noinput

# Django migrate ishga tushirish
echo "🧱 Migrate"
python3 manage.py migrate --noinput

# Celery worker ishga tushirish
echo "🐴 Starting Celery worker"
celery -A config worker --loglevel=info &

# Celery beat ishga tushirish
echo "⏰ Starting Celery beat"
celery -A config beat --loglevel=info &

# Uvicorn ishga tushirish (main web server)
echo "🚀 Starting Uvicorn"
uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --reload --reload-dir core --reload-dir config

# Barcha background processlarni kutish
wait
