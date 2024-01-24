#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Start Gunicorn
gunicorn --bind=20.119.16.56:80 --timeout 600 belonging.wsgi:application
