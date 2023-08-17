# from __future__ import absolute_import , unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NCC.settings')

app = Celery("NCC")
app.conf.enable_utc = False

app.conf.update(timezone = "Asia/Kolkata")
# read config from Django settings, the CELERY namespace would make celery 
# config keys has `CELERY` prefix
app.config_from_object(settings, namespace='CELERY')

# # load tasks.py in django apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind = True)
def debug_task(self):
   print('Request: {0!r}'.format(self.request))





# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery
# # setting the Django settings module.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_task.settings')
# app = Celery('NCC')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# # Looks up for task modules in Django applications and loads them
# app.autodiscover_tasks()
