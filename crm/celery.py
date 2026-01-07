from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# ضبط settings Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')

app = Celery('crm')

# تحميل إعدادات Celery من settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# اكتشاف المهام من كل التطبيقات تلقائيًا
app.autodiscover_tasks()  #tasks is the file name where celery tasks are defined and 
                          # celery will look for tasks.py file in each app folder automatically and 
                          # send it to redis broker for processing then executing with worker
