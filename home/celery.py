from celery import Celery

app = Celery('home')

app.config_from_object('django.conf:settings', namespace='CELERY')