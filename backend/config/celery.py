import os
import environ

from pathlib import Path
from celery import Celery

from django.apps import apps

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent

env = environ.Env()
env.read_env(env_file=str(ROOT_DIR / ".env"))

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', env.str('DJANGO_SETTINGS_MODULE'))

app = Celery('backend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
