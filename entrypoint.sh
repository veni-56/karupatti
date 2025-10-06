#!/bin/bash
set -o errexit

# Navigate to app root
cd /app

# Run Django setup
python manage.py migrate
python manage.py collectstatic --noinput

# Start Gunicorn
gunicorn karupatti_shop.wsgi:application --bind 0.0.0.0:$PORT
