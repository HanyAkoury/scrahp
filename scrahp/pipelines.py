# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os
import pdb
import re
import sqlite3
import string
from typing import List

from itemadapter import ItemAdapter
from scrapy.spiders import Spider
from unidecode import unidecode

from scrahp.items import Article, Url


class UrlPipeline:
    def process_item(self, item: Url, spider: Spider) -> Url:
        return self.cleanup_item(item, spider)

    def cleanup_item(self, item: Url, spider: Spider) -> Url:
        # cleanup title because its a list we need a string
        item["title"] = self.cleanup_title(item, spider)
        item["url"] = self.cleanup_url(item, spider)
        item["base_url"] = item["base_url"][-1]
        return item

    def cleanup_title(self, item: Url, spider: Spider) -> str:
        # cleanup title because its a list we need a string
        return item["title"][-1]

    def cleanup_url(self, item: Url, spider: Spider) -> str:
        # cleanup url for the link to be clickable
        # get base url (news, sport or other etc.)
        if self.is_valid_http_url(item["url"][-1]):
            cleaned_url = item["url"][-1]
        else:
            cleaned_url = f"{item['base_url'][-1]}{item['url'][-1]}"
        return cleaned_url

    def is_valid_http_url(self, url: str) -> bool:
        # Define a regular expression pattern for a valid HTTP or HTTPS URL
        url_pattern = re.compile(
            r"^(https?://)?"  # http:// or https://
            r"([a-zA-Z0-9-]+\.){1,}[a-zA-Z]{2,}(\/[^\s]*)?$",
            re.IGNORECASE,
        )

        return re.match(url_pattern, url) is not None


class ArticlePipeline:
    def process_item(self, item: Article, spider: Spider) -> Article:
        return self.cleanup_item(item, spider)

    def cleanup_item(self, item: Article, spider: Spider) -> Article:
        item["content"] = self.clean_content(item["content"])
        item["url"] = self.clean_url(item["url"])
        item["title"] = self.clean_title(item["title"])
        item["author"] = self.clean_author(item["author"])
        # pdb.set_trace()
        return item

    def clean_content(self, content: List[str]) -> str:
        article_raw_content = [item.strip() for item in content]
        article_content = [item + "." if not item.endswith(tuple(string.punctuation)) else item for item in article_raw_content]
        article_content_string = " ".join(article_content)

        return unidecode(article_content_string).replace("\\", "")

    def clean_url(self, url: List[str]) -> str:
        cleaned_url = [url.strip() for url in url]
        article_content_string = "".join(cleaned_url)

        return article_content_string

    def clean_title(self, title: List[str]) -> str:
        return title[-1]

    def clean_author(self, author: List[str]) -> str:
        return author[-1]


class JsonUrlWriterPipeline:
    def open_spider(self, spider: Spider) -> None:
        if not os.path.exists("data"):
            os.makedirs("data")

        self.file = open("./data/urls.jsonl", "w")

    def close_spider(self, spider: Spider) -> None:
        self.file.close()

    def process_item(self, item: Article, spider: Spider) -> Url:
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item


class JsonArticleWriterPipeline:
    def open_spider(self, spider: Spider) -> None:
        if not os.path.exists("data"):
            os.makedirs("data")

        self.file = open("./data/articles.jsonl", "w")

    def close_spider(self, spider: Spider) -> None:
        self.file.close()

    def process_item(self, item: Url, spider: Spider) -> Url:
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item


class SQLitePipeline:
    def __init__(self) -> None:
        self.db_file = "db/scrahp.db"

    def open_spider(self, spider: Spider) -> None:
        try:
            # Connect to the SQLite database
            self.conn = sqlite3.connect(self.db_file)
            self.c = self.conn.cursor()
        except sqlite3.OperationalError:
            print(f"Database file '{self.db_file}' does not exist. Skipping database operations.")

    def close_spider(self, spider: Spider) -> None:
        if hasattr(self, "conn"):
            # Commit the changes and close the connection
            self.conn.commit()
            self.conn.close()

    def process_item(self, item: Url, spider: Spider) -> Url:
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
