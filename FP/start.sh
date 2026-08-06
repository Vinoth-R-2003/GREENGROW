#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

# Run database migrations before starting the app.
python manage.py migrate --noinput

# Collect static files for WhiteNoise/production serving.
python manage.py collectstatic --noinput

# Start the application with Gunicorn.
exec gunicorn app_core.wsgi:application --bind 0.0.0.0:${PORT} --workers 2
