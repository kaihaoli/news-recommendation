# -*- coding: utf-8 -*-

import os
import sys

from newspaper import Article

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

import cnn_news_scraper
from cloudAMQP_client import CloudAMQPClient

# Use your own Cloud AMQP queue
DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://bddugymf:6Vf5lxc4tfV8HHP1MSPJO3yzhl_iGlVR@eagle.rmq.cloudamqp.com/bddugymf"
DEDUPE_NEWS_TASK_QUEUE_NAME = "tap-news-dedupe-news-task-queue"
SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://bddugymf:6Vf5lxc4tfV8HHP1MSPJO3yzhl_iGlVR@eagle.rmq.cloudamqp.com/bddugymf"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tap-news-scrape-news-task-queue"

SLEEP_TIME_IN_SECONDS = 10

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print 'message is broken'
        return
    task = msg

    # Use newspaper to download & parse url
    article = Article(task['url'])
    article.download()
    article.parse()

    #print article.text

    task['text'] = article.text

    # Send task to Deduple MQ
    dedupe_news_queue_client.sendMessage(task)

while True:
    # Fetch Message from Scape MQ
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.getMessage()
        if msg is not None:
            # Handle message
            try:
                handle_message(msg)
            except Exception as e:
                print e
                pass
        scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)
