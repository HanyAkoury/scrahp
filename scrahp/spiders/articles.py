from pathlib import Path
import scrapy
import json
import pdb
import string
import re
from unidecode import unidecode

from ..items import Article
from ..loaders import Loader


class ArticlesSpider(scrapy.Spider):
    """
    Spider that can crawl the website and try to get the different articles from the website.
    The idea is to crawl and store the articles as well as their urls inside a json, that will serve
    as an url inputs to scrap for more information about the said articles.
    """

    name = "articles"
    custom_settings = {
        "ITEM_PIPELINES": {
            "scrahp.pipelines.ArticlePipeline": 300,
            "scrahp.pipelines.JsonWriterPipeline2": 400,
        }
    }
    url_location = "./data/urls.jsonl"
    local_urls = []
    author_queries = [
        "div.ssrcss-68pt20-Text-TextContributorName ::text",
        "div.author-unit ::text",
        "div.ssrcss-h3c0s8-ContributorContainer ::text",
        "div.qa-contributor-name ::text",
        "div.qa-story-contributor ::text",
    ]

    content_queries = [
        "div.ssrcss-11r1m41-RichTextComponentWrapper ::text, h2.ssrcss-y2fd7s-StyledHeading ::text",
        "div.article__body-content ::text",
        "div.qa-story-body ::text",
    ]

    def start_requests(self):
        articles_urls = self.load_jsonl_file(self.url_location)

        for url in articles_urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # self.save_page_offline(response=response)

        loader = Loader(item=Article(), selector=response)

        loader.add_css("title", "h1::text")
        loader.add_value("url", response.url)
        self.add_key(response, loader, self.author_queries, "author")
        self.add_key(response, loader, self.content_queries, "content")

        yield loader.load_item()

    def save_page_offline(self, response) -> None:
        page = response.url.split("/")[-2]
        directory = "./pages/"
        filename = f"{directory}Articles2-{page}.html"

        # Create the directory if it doesn"t exist
        Path(directory).mkdir(parents=True, exist_ok=True)

        with open(filename, "wb") as file:
            file.write(response.body)

        self.local_urls.append(filename)
        self.log(f"Saved file {filename}")

    def load_jsonl_file(self, file_path):
        data = []
        with open(file_path, "r") as file:
            for line in file:
                item = json.loads(line)
                data.append(item)

        data = self.filter_urls(data)
        return data

    def filter_urls(self, url_json):
        # If url has /av/ remove
        # If url has /live/ remove
        # IF url is in unwanted urls remove
        # pdb.set_trace()
        callable_urls = []
        unwanted_urls = [
            "https://www.bbc.com/news/world_radio_and_tv",
            "https://www.bbc.com/sounds/play/live:bbc_world_service",
        ]

        for line in url_json:
            if line["url"] in unwanted_urls:
                print(line)
            elif "/av/" in str(line["url"]):
                print(line)
            elif "/live" in str(line["url"]):
                print(line)
            else:
                callable_urls.append(line["url"])
        # pdb.set_trace()
        return callable_urls

    def extractable_content(self, response, css_queries) -> None:
        # pdb.set_trace()
        for query in css_queries:
            if len(response.css(query)) > 0:
                return query
        return None

    def add_key(self, response, loader: Loader, queries, item) -> None:
        # pdb.set_trace()
        potential_key = self.extractable_content(response, queries)
        if potential_key is not None:
            loader.add_css(item, potential_key)
        else:
            loader.add_value(item, ["n/a"])
