from __future__ import absolute_import

from time import sleep
from django.core.cache import cache
from celery import shared_task
from celery.signals import worker_process_init

from crawl import run_spider, run_ig


acquire_lock = lambda lock_id: cache.add(lock_id, 'true', 60)
release_lock = lambda lock_id: cache.delete(lock_id)


@shared_task
def fetch_fb(task_entry):
    lock_id = 'fb_lock'

    while True:
        if acquire_lock(lock_id):
            try:
                run_spider(task_entry)
            finally:
                release_lock(lock_id)
                break

        sleep(5)
    return


@shared_task
def fetch_ig(task_entry, token):
    lock_id = 'ig_lock'

    while True:
        if acquire_lock(lock_id):
            try:
                run_ig(task_entry, token)
            finally:
                release_lock(lock_id)
                break

        sleep(5)
    return
