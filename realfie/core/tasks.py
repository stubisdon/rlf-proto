from __future__ import absolute_import

from celery import shared_task
from celery.signals import worker_process_init

from crawl import run_spider


@shared_task
def fetch_fb(task_entry):
    run_spider(task_entry)
    return
