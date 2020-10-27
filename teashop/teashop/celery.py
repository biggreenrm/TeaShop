import os
from celery import Celery


# set the enviroment's variable, thar consist the name of settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teashop.settings')

app = Celery('teashop')

# it gives an ability to set CELERY settings in settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# process of finding and loading async tasks (find all tasks.py)
app.autodiscover_tasks()