# !/usr/bin/env python
# An app that publishes daily trending cryptocurrency news from around the web.
# Author <expl00ra>
# Copyright(c) 2018
# MIT License

import os

from telegram.ext import Updater
import feedparser as fp
from emoji import emojize

class Aggregator:
    """
    Collects information from different sources and processes
    them to desired format.
    - Currently supports Markdown only


    """
    def __init__(self):
        self.bitcoin_news_rss = "http://bitcoin.worldnewsoffice.com/rss/category/1"
        self.altcoin_news_rss = "http://bitcoin.worldnewsoffice.com/rss/category/2"

    def get_news(self):
        """
        Returns a list of lists of bitcoin and altcoin news
        """
        bitcoin_news = fp.parse(self.bitcoin_news_rss)['entries'][:4]
        altcoin_news = fp.parse(self.altcoin_news_rss)['entries'][:4]

        return [bitcoin_news, altcoin_news]

    def get_link(self, source):
        "Cleans source string to generate original link"
        if "=" in source:
            return source.split("=")[1]
        else:
            return source

    def generate_message(self):
        """
        Generates template for news
        """
        news_group = self.get_news()
        bitcoin_news = news_group[0]
        altcoin_news = news_group[1]
        # grapes emoji
        grapes = emojize(':grapes:')

        news_item = "{} *{}* - [Read more >>]({})\n"
        bitcoin_news_list = []
        altcoin_news_list = []

        for news in bitcoin_news:
            bitcoin_news_list.append(
                news_item.format(
                    grapes,
                    news.title,
                    self.get_link(news.source),
                )
            )

        for news_item in altcoin_news:
            bitcoin_news_list.append(
                news_item.format(
                    grapes,
                    news_item.title,
                    self.get_link(news_item.source),
                )
            )

        bitcoin_news_message = " ".join(bitcoin_news_list)
        altcoin_news_message = " ".join(altcoin_news_list)
        full_message = [bitcoin_news_message, altcoin_news_message]

        return " ".join(full_message)

    def get_markdown(self):
        """
        Returns markdown version of aggregated news
        ready for publishing
        """
        heading = "*Latest news from the last 24hrs*\n"
        footer = "powered by @bitletter"
        news = self.generate_message()

        news_md = """
{}

{}

{}
""".format(heading, news, footer)
        return news_md

        
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
        chat_id='@testayowachannel',
        parse_mode='Markdown',
        text=news
    )

job_minute = job_queue.run_repeating(send_letter, interval=20, first=5)

# if __name__ == '__main__':
#     updater.start_polling()
