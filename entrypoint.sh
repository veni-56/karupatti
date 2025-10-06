#!/bin/bash
set -o errexit

#Django commands
python manage.py migrate
python manage.py collectstatics

#start server
gunicorn karupatti_shop.wsgi:application
--bind 0.0.0.0:8000