"""
WSGI config for kocham_wode_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import environ

from django.core.wsgi import get_wsgi_application

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(BASE_DIR, '.env')

env = environ.Env()
environ.Env.read_env(env_path)

settings_location = env('DJANGO_SETTINGS_MODULE')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_location)

application = get_wsgi_application()
