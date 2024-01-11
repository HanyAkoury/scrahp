import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import scrapy
from scrapy.http import Response

from ..items import Article
from ..loaders import Loader


class ArticlesSpider(scrapy.Spider):
    """
    Spider that can crawl the website and try to get the different articles from the website.
    The idea is to crawl and store the articles as well as their urls inside a json, that will serve
    as an url inputs to scrap for more information about the said articles.
    """

    name: str = "articles"
    custom_settings: Optional[Dict[str, Dict[str, int]]] = {
        "ITEM_PIPELINES": {
            "scrahp.pipelines.ArticlePipeline": 300,
            "scrahp.pipelines.JsonArticleWriterPipeline": 400,
        }
    }
    url_location: str = "./data/urls.jsonl"
    local_urls: List[str] = []
    author_queries: list[str] = [
        "div.ssrcss-68pt20-Text-TextContributorName ::text",
        "div.author-unit ::text",
        "div.ssrcss-h3c0s8-ContributorContainer ::text",
        "div.qa-contributor-name ::text",
        "div.qa-story-contributor ::text",
    ]

    content_queries: List[str] = [
        "div.ssrcss-11r1m41-RichTextComponentWrapper ::text,\
              h2.ssrcss-y2fd7s-StyledHeading ::text",
        "div.article__body-content ::text",
        "div.qa-story-body ::text",
    ]

    def start_requests(self) -> Any:
        articles_urls: List[str] = self.load_jsonl_file(self.url_location)

        for url in articles_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: Response, **kwargs: Any) -> Any:
        # self.save_page_offline(response=response)

        loader: Loader = Loader(item=Article(), selector=response)

        if self.is_usable_url(response.url):
            loader.add_css("title", "h1::text")
            loader.add_value("url", response.url)
            self.add_key(response=response, loader=loader, queries=self.author_queries, key="author")
            self.add_key(response=response, loader=loader, queries=self.content_queries, key="content")
            yield loader.load_item()

    def save_page_offline(self, response: Response) -> None:
        page = response.url.split("/")[-2]
        directory = "./pages/"
        filename = f"{directory}Articles2-{page}.html"

        # Create the directory if it doesn"t exist
        Path(directory).mkdir(parents=True, exist_ok=True)

        with open(filename, "wb") as file:
            file.write(response.body)

        self.local_urls.append(filename)
        self.log(f"Saved file {filename}")

    def load_jsonl_file(self, file_path: str) -> List[str]:
        data: List[Dict[str, str]] = []
        with open(file_path, "r") as file:
            for line in file:
                item = json.loads(line)
                data.append(item)
        return [line["url"] for line in data]

    def is_usable_url(self, url: str) -> bool:
        unwanted_urls = [
            "https://www.bbc.com/news/world_radio_and_tv",
            "https://www.bbc.com/sounds/play/live:bbc_world_service",
        ]
        if url in unwanted_urls:
            return False
        elif "/av/" in str(url):
            return False
        elif "/live" in str(url):
            return False
        elif "/videos/" in str(url):
            return False
        else:
            return True

    def extractable_content(self, response: Response, css_queries: List[str]) -> Optional[str]:
        for query in css_queries:
            if len(response.css(query)) > 0:
                return query
        return None

    def add_key(self, response: Response, loader: Loader, queries: List[str], key: str) -> None:
        potential_key = self.extractable_content(response, queries)
        if potential_key is not None:
            loader.add_css(key, potential_key)
        else:
            loader.add_value(key, "n/a")
