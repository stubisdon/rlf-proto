# -*- coding: utf-8 -*-

# Scrapy settings for rlfspider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

BOT_NAME = 'rlfspider'

SPIDER_MODULES = ['rlfspider.spiders']
NEWSPIDER_MODULE = 'rlfspider.spiders'

USER_AGENT = 'Realfie/1.0'
MEMUSAGE_REPORT = True

LOG_LEVEL = 'INFO'
LOG_FILE = '{0}.log'.format(BOT_NAME)
#LOG_STDOUT = True

ITEM_PIPELINES = {
    'rlfspider.pipelines.RlfspiderPipeline': 100,
}

DOWNLOAD_DELAY = 0.5
