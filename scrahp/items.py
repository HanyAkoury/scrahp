import scrapy


class Url(scrapy.Item):
    """
    Represents an article's URL and its title.

    Attributes:
        title (scrapy.Field): The title of the article.
        base_url (scrapy.Field): The base URL of the article's website.
        url (scrapy.Field): The full URL of the article.
    """

    title = scrapy.Field()
    base_url = scrapy.Field()
    url = scrapy.Field()


class Article(scrapy.Item):
    """
    Represents detailed information about an article.

    Attributes:
        title (scrapy.Field): The title of the article.
        url (scrapy.Field): The full URL of the article.
        author (scrapy.Field): The author of the article.
        content (scrapy.Field): The full text content of the article.
    """

    title = scrapy.Field()  # Title of the article
    url = scrapy.Field()  # URL of the article
    author = scrapy.Field()  # Author of the article
    content = scrapy.Field()  # Content of the article
