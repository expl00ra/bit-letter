# !/usr/bin/env python
# An app that publishes daily trending cryptocurrency news from around the web.
# Author <expl00ra>
# Copyright(c) 2018
# MIT License

import os
from datetime import time
import logging

from telegram.ext import Updater

from services.aggregator import Aggregator

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )

updater = Updater(os.environ["ACCESS_TOKEN"])
dipatcher = updater.dispatcher

# set up job queue
job_queue = updater.job_queue

def send_letter(bot, job):
    """
    Posts lastes aggregated news to the specified channel
    """
    # set up Aggregator 
    aggregator = Aggregator()
    news = aggregator.get_markdown()
    bot.send_message(
        chat_id='@bitletter',
        parse_mode='Markdown',
        disable_web_page_preview=True,
        text=news
    )

job_minute = job_queue.run_daily(
    send_letter,
    time=time(6, 00),
    )

if __name__ == '__main__':
     updater.start_polling()
