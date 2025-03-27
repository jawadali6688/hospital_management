import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_portal2.settings')

celery_app = Celery('hospital_portal2')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
