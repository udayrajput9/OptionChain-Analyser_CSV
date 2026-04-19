# PythonAnywhere WSGI Configuration
# Place this content in /var/www/udayoption_pythonanywhere_com_wsgi.py

import os
import sys
from pathlib import Path

# Add your project directory to the sys.path
project_home = os.path.expanduser('~/OptionChain-Analyser_CSV')
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment to production
os.environ['DJANGO_SETTINGS_MODULE'] = 'optionchain_project.settings'

# Load environment variables from .env file
env_file = os.path.join(project_home, '.env')
if os.path.exists(env_file):
    from dotenv import load_dotenv
    load_dotenv(env_file)

# Import and get WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
