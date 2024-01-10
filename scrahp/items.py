import scrapy


class Url(scrapy.Item):
    """
    Scrapy Item that holds information about an article's URL and its title
    """

    title = scrapy.Field()
    url = scrapy.Field()


class Article(scrapy.Item):
    """
    Scrapy Item that holds information about an article's URL and its title
    """

    title = scrapy.Field()
    url = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
