import sys
import os
from dj_static import Cling  # Optional, only if serving static files via WSGI

# Add the project directory to sys.path
sys.path.insert(0, os.path.dirname(__file__))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prohelper.settings')

# Import WSGI application
from django.core.wsgi import get_wsgi_application

# Wrap with Cling if serving static files
application = Cling(get_wsgi_application())
