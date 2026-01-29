#!/usr/bin/env bash
# exit on error
set -o errexit

echo "===== Installing Python dependencies ====="
python -m pip install -r requirements.txt

echo "===== Collecting static files ====="
python manage.py collectstatic --no-input

echo "===== Running database migrations ====="
python manage.py migrate --verbosity 2

echo "===== Creating default superuser ====="
python manage.py create_default_superuser

echo "===== Seeding initial data ====="
python seed_data.py

echo "===== Build completed successfully ====="
