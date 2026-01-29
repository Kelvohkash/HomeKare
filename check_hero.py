import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mtaani_project.settings')
django.setup()

from web.models import HeroContent

hero = HeroContent.objects.first()
if hero:
    print(f"Hero exists: {hero.title}")
    print(f"  Image field: {hero.image}")
    if hero.image:
        print(f"  Image URL: {hero.image.url}")
    else:
        print(f"  WARNING: No image uploaded")
else:
    print("WARNING: No HeroContent found - needs to be created in admin")
