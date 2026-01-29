import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mtaani_project.settings')
django.setup()

from django.db import connection

def cleanup():
    with connection.cursor() as cursor:
        # Check migrations
        cursor.execute("SELECT name FROM django_migrations WHERE app='web'")
        migrations = [row[0] for row in cursor.fetchall()]
        print(f"Current migrations in DB: {migrations}")

        # If we have 0008 but not 0009, and tables exist, we are in a ghost state.
        # Let's just try to drop the ghost tables if they exist so migration 0009 can run fresh
        tables_to_drop = ['web_worker', 'web_worker_skills', 'web_workerdocument', 'web_category']
        for table in tables_to_drop:
            try:
                cursor.execute(f"DROP TABLE {table}")
                print(f"Dropped table {table}")
            except Exception as e:
                print(f"Table {table} does not exist or could not be dropped: {e}")

if __name__ == '__main__':
    cleanup()
