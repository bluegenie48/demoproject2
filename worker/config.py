"""Django settings for the worker's ORM access."""

import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'worker_db'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'USER': os.environ.get('DB_USER', 'worker'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
    }
}

INSTALLED_APPS = ['worker']
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'change-me')
