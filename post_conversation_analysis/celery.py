from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'post_conversation_analysis.settings')

app = Celery('post_conversation_analysis')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Schedule: run daily at midnight
app.conf.beat_schedule = {
    'daily-analysis-task': {
        'task': 'analysis.tasks.daily_analyse_new_conversations',
        'schedule': crontab(hour=0, minute=0),
    },
}
