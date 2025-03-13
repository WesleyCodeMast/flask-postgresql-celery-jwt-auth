from celery import Celery
from celery.signals import setup_logging
from celery.schedules import crontab

from core.settings import get_application_settings
from .utils import application_modules

import asyncio
import ast

settings = get_application_settings()
app = Celery(
    'TeleHealth', 
    broker=settings.CELERY_BROKER_URL,
)
app.config_from_object(settings.celery_settings)
app.autodiscover_tasks(application_modules(), force=True)

app.conf.timezone = 'America/New_York'  # EST timezone

@app.on_after_finalize.connect
def _on_celery_startup(sender, **kwargs):
    from core.db import setup_database_service_sync, setup_database_service

    setup_database_service_sync(settings)
    asyncio.run(setup_database_service(settings))

__all__ = (
    'app',
)
