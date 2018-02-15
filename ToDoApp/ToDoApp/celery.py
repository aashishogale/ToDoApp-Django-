import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
\
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ToDoApp.settings')

app = Celery('ToDoApp')
app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_tasks()

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#      app.add_periodic_task(10.0, print1.print(), name='add every 10')

# @app.task
# def print1():
#     print("enter the method")

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'Todo.views.deleteArchivedNotes',
        'schedule':30.0
       
    },
}

app.conf.update(
        CELERY_TIMEZONE = 'Asia/Kolkata'   # set timezone in here
        )
