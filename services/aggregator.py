from emoji import emojize
import feedparser as fp

class Aggregator:
    """
    Collects information from different sources and processes
    them to desired format.
    - Currently supports Markdown only


    """
    def __init__(self):
        self.bitcoin_news_rss = "http://bitcoin.worldnewsoffice.com/rss/category/1"
        self.altcoin_news_rss = "http://bitcoin.worldnewsoffice.com/rss/category/2"
        # grapes emoji
        self.grapes = emojize(':grapes:')

    def get_news(self):
        """
        Returns a list of lists of bitcoin and altcoin news
        """
        bitcoin_news = fp.parse(self.bitcoin_news_rss)['entries'][:4]
        altcoin_news = fp.parse(self.altcoin_news_rss)['entries'][:4]

        return [bitcoin_news, altcoin_news]

    def _get_link(self, source):
        "Cleans source string to generate original link"
        if "=" in source:
            print(source)
            return source.split("=")[1]
        else:
            return source

    def _process_raw_news(self, raw_news, processed_news, news_format):
        """
        Processes template and loads in refined data
        """
        for news in raw_news:
                processed_news.append(
                    news_format.format(
                        self.grapes,
                        news.title,
                        self._get_link(news.source.title),
                    )
                )

    def generate_message(self):
        """
        Generates template for news
        """
        news_group = self.get_news()
        bitcoin_news = news_group[0]
        altcoin_news = news_group[1]
        

        news_item = "{} *{}* - [Read more >>]({}) \n\n"
        bitcoin_news_list = []
        altcoin_news_list = []

        self._process_raw_news(bitcoin_news, bitcoin_news_list, news_item)
        self._process_raw_news(altcoin_news, altcoin_news_list, news_item)

        bitcoin_news_message = " ".join(bitcoin_news_list)
        altcoin_news_message = " ".join(altcoin_news_list)
        full_message = [bitcoin_news_message, altcoin_news_message]

        return " ".join(full_message)

    def get_markdown(self):
        """
        Returns markdown version of aggregated news
        ready for publishing
        """
        heading = "_Latest news from the last 24hrs_"
        news = self.generate_message()
        footer = "powered by @bitletter"
        

        news_md = """
{}

{}
{}
""".format(heading, news, footer)
        return news_md