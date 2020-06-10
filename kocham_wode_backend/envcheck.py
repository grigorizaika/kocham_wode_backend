#!/home/ubuntu/.virtualenvs/kochamwodeenv/bin/python
import os
import environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env_path = os.path.join(BASE_DIR, '.env')
env = environ.Env()
environ.Env.read_env(env_path)

print(env('DJANGO_SETTINGS_MODULE'))



