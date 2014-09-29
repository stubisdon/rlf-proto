from __future__ import absolute_import

from celery import shared_task
from celery.signals import worker_process_init

from crawl import run_spider


@shared_task
def test_search(rlf_user):
    run_spider(rlf_user)
    return
