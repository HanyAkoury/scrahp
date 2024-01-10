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

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from unidecode import unidecode


class UrlPipeline:
    def process_item(self, item, spider):
        return self.cleanup_item(item, spider)

    def cleanup_item(self, item, spider):
        # cleanup title because its a list we need a string
        item["title"] = self.cleanup_title(item, spider)
        item["url"] = self.cleanup_url(item, spider)
        return item

    def cleanup_title(self, item, spider):
        # cleanup title because its a list we need a string
        return item["title"][-1]

    def cleanup_url(self, item, spider):
        # cleanup url for the link to be clickable
        # pdb.set_trace()
        base_url = re.search(r"(https?://[^/]+)", spider.url[-1]).group(1)
        if self.is_valid_http_url(item["url"][-1]):
            cleaned_url = item["url"][-1]
        else:
            cleaned_url = f"{base_url}{item['url'][-1]}"
        return cleaned_url

    def is_valid_http_url(self, url):
        # Define a regular expression pattern for a valid HTTP or HTTPS URL
        url_pattern = re.compile(
            r"^(https?://)?"  # http:// or https://
            r"([a-zA-Z0-9-]+\.){1,}[a-zA-Z]{2,}(\/[^\s]*)?$",
            re.IGNORECASE,
        )

        return re.match(url_pattern, url) is not None


class ArticlePipeline:
    def process_item(self, item, spider):
        # pdb.set_trace()
        return self.cleanup_item(item, spider)

    def cleanup_item(self, item, spider):
        # pdb.set_trace()
        item["content"] = self.clean_article_content(item["content"])
        item["url"] = self.clean_url(item["url"])
        return item

    def clean_article_content(self, content):
        article_raw_content = [item.strip() for item in content]
        article_content = [
            item + "." if not item.endswith(tuple(string.punctuation)) else item
            for item in article_raw_content
        ]
        article_content_string = " ".join(article_content)

        return unidecode(article_content_string).replace("\\", "")

    def clean_url(self, url):
        # pdb.set_trace()
        cleaned_url = [url.strip() for url in url]
        article_content_string = "".join(cleaned_url)
        return article_content_string


class JsonWriterPipeline:
    def open_spider(self, spider):
        if not os.path.exists("data"):
            os.makedirs("data")

        self.file = open("./data/urls.jsonl", "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        print("---")
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item


class JsonWriterPipeline2:
    def open_spider(self, spider):
        if not os.path.exists("data"):
            os.makedirs("data")

        self.file = open("./data/articles.jsonl", "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        print("---")
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item


class SQLitePipeline:
    def __init__(self):
        self.db_file = "db/scrahp.db"

    def open_spider(self, spider):
        try:
            # Connect to the SQLite database
            self.conn = sqlite3.connect(self.db_file)
            self.c = self.conn.cursor()
        except sqlite3.OperationalError:
            print(
                f"Database file '{self.db_file}' does not exist. Skipping database operations."
            )

    def close_spider(self, spider):
        if hasattr(self, "conn"):
            # Commit the changes and close the connection
            self.conn.commit()
            self.conn.close()

    def process_item(self, item, spider):
        if not hasattr(self, "conn"):
            return item

        # Insert the article into the database, ignoring duplicates based on the URL
        self.c.execute(
            """
            INSERT OR IGNORE INTO articles (title, url)
            VALUES (?, ?)
        """,
            (item["title"], item["url"]),
        )

        return item
