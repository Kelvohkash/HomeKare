import os
import sys
import django

# Set up project root in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mtaani_project.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def setup_google_app():
    # Ensure the default site has the correct domain/name
    site, created = Site.objects.get_or_create(id=1, defaults={'domain': '127.0.0.1:8000', 'name': 'Mtaani Connect'})
    if not created:
        site.domain = '127.0.0.1:8000'
        site.name = 'Mtaani Connect'
        site.save()
        print(f"Updated Site: {site.domain}")
    else:
        print(f"Created Site: {site.domain}")

    # Create the SocialApp for Google
    app, created = SocialApp.objects.get_or_create(
        provider='google',
        defaults={
            'name': 'Google Login',
            'client_id': 'placeholder-client-id.apps.googleusercontent.com',
            'secret': 'placeholder-secret',
        }
    )
    
    # Associate the app with the site
    app.sites.add(site)
    
    if created:
        print("Successfully created Google SocialApp (with placeholders).")
    else:
        print("Google SocialApp already exists.")

if __name__ == "__main__":
    try:
        setup_google_app()
    except Exception as e:
        print(f"Error setting up SocialApp: {e}")
