import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'belonging.settings')

print("WSGI application loaded")  # Add this line
application = get_wsgi_application()
