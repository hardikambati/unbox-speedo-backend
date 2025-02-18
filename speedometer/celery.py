from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "speedometer.settings")

app = Celery("speedometer")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(packages=["utils"], related_name="celery.tasks")

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
