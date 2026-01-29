import os
import sys
from pathlib import Path

# Add the project root to sys.path to ensure local modules are found
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# If the project is actually inside a subdirectory (based on earlier logs/checks)
SUB_DIR = BASE_DIR / "Mtaani Connect James"
if SUB_DIR.exists() and (SUB_DIR / "mtaani_project").exists():
    if str(SUB_DIR) not in sys.path:
        sys.path.insert(0, str(SUB_DIR))

# Debugging information for logs
print(f"--- Deployment Environment Check ---")
print(f"Current Working Directory: {os.getcwd()}")
print(f"Python sys.path: {sys.path}")
print(f"Files in root: {os.listdir(BASE_DIR)[:10]}...") # Print first 10 files
if SUB_DIR.exists():
    print(f"Files in subdirectory '{SUB_DIR.name}': {os.listdir(SUB_DIR)[:10]}...")

from django.core.wsgi import get_wsgi_application

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mtaani_project.settings')

try:
    application = get_wsgi_application()
    # Alias 'app' for platforms expecting it
    app = application
    print("WSGI application loaded successfully.")
except Exception as e:
    print(f"Error loading WSGI application: {e}")
    # Potentially useful traceback for debugging
    import traceback
    traceback.print_exc()
    raise e
