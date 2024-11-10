import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab
from celery.signals import setup_logging  # noqa

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bitArticles.settings')

app = Celery('bitArticles')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


@setup_logging.connect
def config_loggers(*args, **kwargs):
    from logging.config import dictConfig  # noqa
    from django.conf import settings  # noqa

    dictConfig(settings.LOGGING)


# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # executes every 30 seconds
    'periodic-scheduled-article-stat-calculation': {
        'task': 'article.tasks.find_and_execute_article_stats_calculation_task',
        'schedule': timedelta(seconds=30),  # should be configured
    },
    'periodic-scheduled-article-suspicious-score-calculation': {
        'task': 'article.tasks.find_and_execute_article_suspicious_score_task',
        'schedule': timedelta(minutes=10),  # should be configured
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
