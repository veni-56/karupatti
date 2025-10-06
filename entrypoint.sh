#!/bin/bash
set -o errexit

# Move into Django project folder
cd /app/django_backend

# Django commands
python manage.py migrate
python manage.py collectstatic --noinput

# Start Gunicorn server
gunicorn karupatti_shop.wsgi:application --bind 0.0.0.0:$PORT
