#! /usr/bin/env bash

set -o errexit   #  exit on error

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py makemigrations account
python manage.py makemigrations product
python manage.py migrate

# Create superuser
python manage.py shell << END
from account.models import Account
import os

email = os.getenv("DJANGO_SUPERUSER_EMAIL", "araile@gmail.com")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "bavtwany")

if not Account.objects.filter(email=email).exists():
    Account.objects.create_superuser(email=email, password=password)
    print("Superuser created")
else:
    print("Superuser already exists")
END
