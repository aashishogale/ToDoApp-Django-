import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
\
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ToDoApp.settings')

app = Celery('ToDoApp')
app.config_from_object('django.conf:settings')


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#      app.add_periodic_task(10.0, print1.print(), name='add every 10')

# @app.task
# def print1():

#     print("enter the method")

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'Todo.views.deleteArchivedNotes',
        'schedule': 30.0

    },
}

app.conf.update(
    CELERY_TIMEZONE='Asia/Kolkata'   # set timezone in here
)
app.conf.database_engine_options = {

}

# from django_celery_beat.models import CrontabSchedule, PeriodicTask

# schedule,_= CrontabSchedule.objects.get_or_create(
#     minute='1',
#     hour='*',
#     day_of_week='*',
#     day_of_month='*',   month_of_year='*',
# )
# from django_celery_beat.models import PeriodicTask, IntervalSchedule
# PeriodicTask.objects.create(
#     crontab=schedule,
#     name='Importing contacts',
#     task='Todo.views.deleteArchivedNotes',
# )
