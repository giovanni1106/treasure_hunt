from decouple import config
import django

django.setup()

from django.contrib.auth.models import User


ADMIN_USERNAME = config("DJANGO_ADMIN_USERNAME", default="admin")
ADMIN_PASSWORD = config("DJANGO_ADMIN_PASSWORD", default="adminpassword")
ADMIN_EMAIL = config("DJANGO_ADMIN_EMAIL", default="admin@example.com")

if not User.objects.filter(username=ADMIN_USERNAME).exists():
    User.objects.create_superuser(ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD)
    print(f"Superuser '{ADMIN_USERNAME}' created successfully.")
else:
    print(f"Superuser '{ADMIN_USERNAME}' already exists.")
