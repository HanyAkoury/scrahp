# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Article(scrapy.Item):
    """
    title
    field
    Args:
        scrapy (_type_): _description_
    """
    title = scrapy.Field()
    url = scrapy.Field()
    # author = scrapy.Field()
    # headline = scrapy.Field()
    # article_text = scrapy.Field()
