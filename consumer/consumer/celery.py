import os
import logging
from celery import Celery, signals


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "consumer.settings")
app = Celery("consumer.data_consumer")
app.config_from_object("django.conf:settings", namespace="CELERY")


# Define a function to be called after the logger is set up
def customize_logger(loglevel, logfile, format, colorize, **kwargs):
    # Get the logger object created by Celery
    logger = logging.getLogger("celery")
    logger.setLevel(logging.DEBUG)


# Connect the customize_logger function to the after_setup_logger signal
signals.after_setup_logger.connect(customize_logger)

app.autodiscover_tasks()
