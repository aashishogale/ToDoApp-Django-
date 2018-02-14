import os
from celery import Celery
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ToDoApp.settings')

app = Celery('ToDoApp')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#      app.add_periodic_task(10.0, print1.print(), name='add every 10')

# @app.task
# def print1():
#     print("enter the method")

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'Todo.tasks.print2',
        'schedule': 30.0,
       
    },
}