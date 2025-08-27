#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Beneath_the_blue.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

# In Django shell (python manage.py shell)
from django.contrib.auth import get_user_model
User = get_user_model()

# Find duplicate emails
from django.db.models import Count
duplicates = User.objects.values('email').annotate(email_count=Count('email')).filter(email_count__gt=1)
print(duplicates)