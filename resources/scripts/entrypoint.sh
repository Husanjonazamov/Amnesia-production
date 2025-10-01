#!/bin/bash


while ! nc -z db 5432; do
  sleep 2
  echo "Waiting postgress...."
done

echo "📦 Collectstatic"
python3 manage.py collectstatic --noinput

echo "🧱 Migrate"
python3 manage.py migrate --noinput


echo "☕ Starting Celery worker and beat"
celery -A config  worker -B --loglevel=info &

echo "🚀 Uvicorn"
uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --reload --reload-dir core --reload-dir config

wait
