#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Start Gunicorn
gunicorn --bind=0.0.0.0 --timeout 600 belonging.wsgi.application
