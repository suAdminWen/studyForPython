from celery import Celery

app = Celery('celery_app')

app.config_from_object('celery_app.config')