import os
from django.core.wsgi import get_wsgi_application

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mtaani_project.settings')

# Get the WSGI application
application = get_wsgi_application()

# Alias 'app' to 'application' because some platforms (like Render's default) 
# look for an object named 'app' in a file named 'app.py'
app = application
