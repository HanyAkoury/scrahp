import json
import os

import re
import sqlite3
import string
from typing import List, Union

from itemadapter import ItemAdapter
from scrapy.spiders import Spider
from unidecode import unidecode

from scrahp.items import Article, Url


class UrlPipeline:
    """
    Pipeline for processing and cleaning up Url items.

    Methods in this class are responsible for standardizing and cleaning the data
    in the Url items scraped by the spiders.
    """

    def process_item(self, item: Url, spider: Spider) -> Url:
        """
        Process and clean up a Url item.

        Args:
            item (Url): The Url item to process.
            spider (Spider): The spider that scraped the item.

        Returns:
            Url: The cleaned up item.
        """
        return self.cleanup_item(item, spider)

    def cleanup_item(self, item: Url, spider: Spider) -> Url:
        """
        Clean up the fields of a 'Url' item.
        Specific cleaning actions are performed on title, URL, and base URL of the item.

        Args:
            item (Url): The 'Url' item to clean.
            spider (Spider): The spider that scraped the item.

        Returns:
            Url: The cleaned item.
        """
        item["title"] = self.cleanup_title(item, spider)
        item["url"] = self.cleanup_url(item, spider)
        item["base_url"] = item["base_url"][-1]
        return item

    def cleanup_title(self, item: Url, spider: Spider) -> str:
        """
        Clean up the title field of a 'Url' item.
        This method is responsible for converting the title field from a list to a string.

        Args:
            item (Url): The 'Url' item with the title field.
            spider (Spider): The spider that scraped the item.

        Returns:
            str: The cleaned title.
        """
        return item["title"][-1]

    def cleanup_url(self, item: Url, spider: Spider) -> str:
        """
        Clean up the URL field of a 'Url' item.
        This method can include formatting actions and validation checks.

        Args:
            item (Url): The 'Url' item with the URL field.
            spider (Spider): The spider that scraped the item.

        Returns:
            str: The cleaned URL.
        """
        # cleanup url for the link to be clickable
        # get base url (news, sport or other etc.)
        if self.is_valid_http_url(item["url"][-1]):
            cleaned_url = item["url"][-1]
        else:
            cleaned_url = f"{item['base_url'][-1]}{item['url'][-1]}"
        return cleaned_url

    def is_valid_http_url(self, url: str) -> bool:
        """
        Check if the provided string is a valid HTTP URL.
        This function validates the string to ensure it conforms to the HTTP URL format.

        Args:
            url (str): The URL string to validate.

        Returns:
            bool: True if the URL is valid and follows the HTTP format, False otherwise.
        """
        url_pattern = re.compile(
            r"^(https?://)?"  # http:// or https://
            r"([a-zA-Z0-9-]+\.){1,}[a-zA-Z]{2,}(\/[^\s]*)?$",
            re.IGNORECASE,
        )

        return re.match(url_pattern, url) is not None


class ArticlePipeline:
    """
    A pipeline for processing 'Article' items.

    This pipeline handles tasks such as cleaning, validating, and storing 'Article' items
    scraped by the spiders. Each item processed go through a series of methods
    to ensure data integrity and proper formatting before being passed on.
    """
    def process_item(self, item: Article, spider: Spider) -> Article:
        """
        Process an 'Article' item through the pipeline.
        This method is called for every 'Article' item scraped by the spiders.
        It orchestrates the processing of the item through various methods
        such as validation and cleaning.

        Args:
            item (Article): The 'Article' item to process.
            spider (Spider): The spider that scraped the item.

        Returns:
            Article: The processed item, ready for storage or further processing.
        """
        return self.cleanup_item(item, spider)

    def cleanup_item(self, item: Article, spider: Spider) -> Article:
        """
        Perform general cleanup on an 'Article' item.
        This method orchestrates the cleanup process by calling specific cleaning methods
        for different fields like title, url, author, and content.

        Args:
            item (Article): The 'Article' item to clean.
            spider (Spider): The spider that scraped the item.

        Returns:
            Article: The cleaned article item.
        """
        item["content"] = self.clean_content(item["content"])
        item["url"] = self.clean_url(item["url"])
        item["title"] = self.clean_title(item["title"])
        item["author"] = self.clean_author(item["author"])

        return item

    def clean_content(self, content: List[str]) -> str:
        """
        Clean the content field of an 'Article' item.
        This method performs cleaning operations on the content of the article, such as
        removing extraneous whitespace  or other unwanted characters.

        Args:
            item (Article): The 'Article' item with the content to clean.
            spider (Spider): The spider that scraped the item.

        Returns:
            Article: The item with its content cleaned.
        """
        article_raw_content = [item.strip() for item in content]
        article_content = [item + "." if not item.endswith(tuple(string.punctuation)) else item for item in article_raw_content]
        article_content_string = " ".join(article_content)

        return unidecode(article_content_string).replace("\\", "")

    def clean_url(self, url: List[str]) -> str:
        """
        Standardize and validate the 'url' field of an 'Article' item.
        This method ensures that the URL is in a proper format.

        Args:
            item (Article): The 'Article' item with the url field.
            spider (Spider): The spider that scraped the item.

        Returns:
            str: The standardized and possibly validated URL.
        """
        cleaned_url = [url.strip() for url in url]
        article_content_string = "".join(cleaned_url)

        return article_content_string

    def clean_title(self, title: List[str]) -> str:
        """
        Clean and standardize the 'title' field of an 'Article' item.

        This method is responsible for converting the title field from a list to a string.

        Args:
            item (Article): The 'Article' item with the title field.
            spider (Spider): The spider that scraped the item.

        Returns:
            str: The cleaned and standardized title.
        """
        return title[-1]

    def clean_author(self, author: List[str]) -> str:
        """
        Clean and standardize the 'author' field of an 'Article' item.

        This method is responsible for converting the title field from a list to a string.

        Args:
            item (Article): The 'Article' item with the title field.
            spider (Spider): The spider that scraped the item.

        Returns:
            str: The cleaned author's name.
        """
        # TODO add better cleaning
        return author[-1]

class JsonWriterPipeline:
    """
    A pipeline for writing 'Url' and 'Article' items into separate JSON files.

    Depending on the type of item scraped, this pipeline will write the data into
    either 'data/urls.json' for Url items or 'data/articles.json' for Article items.
    """

    def open_spider(self, spider: Spider):
        """
        Open the spider, initializing the file handlers for URLs and Articles.

        Args:
            spider (Spider): The spider that was opened.
        """
        if not os.path.exists("data"):
            os.makedirs("data")

        mode = 'a' if os.path.exists('data/urls.jsonl') else 'w'
        self.url_file = open('data/urls.jsonl', mode)

        mode = 'a' if os.path.exists('data/articles.jsonl') else 'w'
        self.article_file = open('data/articles.jsonl', mode)

    def close_spider(self, spider: Spider):
        """
        Close the spider, closing the file handlers for URLs and Articles.

        Args:
            spider (Spider): The spider that was closed.
        """
        self.url_file.close()
        self.article_file.close()

    def process_item(self, item: Union[Article, Url], spider: Spider):
        """
        Process the item and write it to the appropriate JSON file.

        Args:
            item (Item): The item scraped by the spider.
            spider (Spider): The spider that scraped the item.

        Returns:
            Item: The item that was processed.
        """
        if isinstance(item, Url):
            line = json.dumps(ItemAdapter(item).asdict()) + "\n"
            self.url_file.write(line)
            return item
        elif isinstance(item, Article):
            line = json.dumps(ItemAdapter(item).asdict()) + "\n"
            self.article_file.write(line)
            return item
        else:
            raise DropItem(f"Unhandled item type: {type(item)}")

class SQLitePipeline:
    def __init__(self) -> None:
        """
        Initialize the SQLitePipeline indicating the database file location.
        """
        self.db_file = "db/scrahp.db"

    def open_spider(self, spider: Spider) -> None:
        """
        Open the spider by connecting the SQLite database.

        Args:
            spider (Spider): The spider that is being opened.
        """
        try:
            # Connect to the SQLite database
            self.conn = sqlite3.connect(self.db_file)
            self.c = self.conn.cursor()
        except sqlite3.OperationalError:
            print(f"Database file '{self.db_file}' does not exist. Skipping database operations.")

    def close_spider(self, spider: Spider) -> None:
        """
        Close the spider - committing changes and closing the database connection.

        Args:
            spider (Spider): The spider that is being closed.
        """
        if hasattr(self, "conn"):
            # Commit the changes and close the connection
            self.conn.commit()
            self.conn.close()

    def process_item(self, item: Url, spider: Spider) -> Url:
        """
        Process every item and insert it into the SQLite database.

        Args:
            item (Url): The item scraped by the spider.
            spider (Spider): The spider that scraped the item.

        Returns:
            Url: The processed item.
        """
        if not hasattr(self, "conn"):
            return item

        # Extract values from the item
        adapter = ItemAdapter(item)

        title = adapter.get("title")
        url = adapter.get("url")
        author = adapter.get("author")
        content = adapter.get("content")

        # Insert the article into the database, ignoring duplicates based on the URL
        self.c.execute("INSERT OR IGNORE INTO articles (title, url, author, content) VALUES (?, ?, ?, ?)", (title, url, author, content))

        return item
