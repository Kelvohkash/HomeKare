"""
Management command to create a default superuser for the admin panel
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Creates a superuser if one does not exist'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@homekare.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Superuser "{username}" created successfully!'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠ Superuser "{username}" already exists.'))
