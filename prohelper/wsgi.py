"""
WSGI config for prohelper project.

It exposes the WSGI callable as a module-level variable named ``application``.
For more information see:
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prohelper.settings')

# Get WSGI application
application = get_wsgi_application()
