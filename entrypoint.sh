#!/bin/sh

# Collect all static files to the root directory
python manage.py collectstatic --no-input

# Start the gunicorn worker processes at the defined port
exec gunicorn core.wsgi:application --bind 0.0.0.0:8080
