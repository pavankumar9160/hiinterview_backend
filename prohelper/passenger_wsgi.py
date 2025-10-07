import sys
import os

# Add your project path to sys.path
sys.path.insert(0, os.path.dirname(__file__))

# Set the settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'prohelper.settings'

# Import Django's WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
