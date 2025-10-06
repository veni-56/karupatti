#!/bin/bash
set -o errexit

cd /app/django_backend

python manage.py migrate
python manage.py collectstatic --noinput

gunicorn karupatti_shop.wsgi:application --bind 0.0.0.0:$PORT
