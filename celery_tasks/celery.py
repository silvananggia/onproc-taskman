# celery_tasks/celery.py

from celery import Celery
from config import settings

app = Celery('celery_tasks',
             broker=settings.CELERY_BROKER_URL,
             backend=settings.CELERY_RESULT_BACKEND,
             include=['celery_tasks.tasks'])

# Optional configuration, see the Celery documentation for more details
app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    worker_concurrency=settings.POLL_INTERVAL,  # Adjust concurrency as needed
)

# Automatically discover tasks from all registered Django apps (if using Django)
# app.autodiscover_tasks()
