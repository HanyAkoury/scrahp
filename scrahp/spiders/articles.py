import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import scrapy
from scrapy.http import Response

from ..items import Article
from ..loaders import Loader


class ArticlesSpider(scrapy.Spider):
    """
    Spider for crawling specified URLs and extracting detailed article information.

    This spider reads article URLs from a JSONL file and crawls each URL to extract
    information such as the title, author, and content of the articles. Extracted data
    is stored in various formats using configured pipelines.
    """

    name: str = "articles"
    custom_settings: Optional[Dict[str, Dict[str, int]]] = {
        "ITEM_PIPELINES": {
            "scrahp.pipelines.ArticlePipeline": 300,
            "scrahp.pipelines.JsonWriterPipeline": 400,
            "scrahp.pipelines.SQLitePipeline": 500,
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
        "a.author-unit__text ::text",
        "div.article__body-content ::text",
        "div.qa-story-body ::text",
        "article.ssrcss-pv1rh6-ArticleWrapper ::text",
    ]

    def start_requests(self) -> Any:
        """
        Generate initial requests from URLs loaded from a JSONL file.
        """
        articles_urls: List[str] = self.load_jsonl_file(self.url_location)

        for url in articles_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: Response, **kwargs: Any) -> Any:
        """
        Parse the response and extract article information using the defined Loader.

        Args:
            response (Response): The response object to parse.

        Yields:
            Item: The extracted article item.
        """
        self.save_page_offline(response=response)

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
        """
        Simple load of URLs from a JSONL file.

        Args:
            file_path (str): Path to the JSONL file.

        Returns:
            List[str]: A list of URLs.
        """
        data: List[Dict[str, str]] = []
        with open(file_path, "r") as file:
            for line in file:
                item = json.loads(line)
                data.append(item)
        return [line["url"] for line in data]

    def is_usable_url(self, url: str) -> bool:
        """
        Check if a URL is suitable for scraping.

        Args:
            url (str): The URL to check.

        Returns:
            bool: True if the URL is suitable, False otherwise.
        """
        unwanted_elements: List[str] = [
            "/av/",
            "/live",
            "/videos/",
            "https://www.bbc.com/news/world_radio_and_tv",
            "https://www.bbc.com/sounds/play/live:bbc_world_service",
        ]
        if any(element.lower() in url.lower() for element in unwanted_elements):
            return False
        else:
            return True

    def extractable_content(self, response: Response, css_queries: List[str]) -> Optional[str]:
        """
        Determine if content is extractable using provided CSS queries.
        Args
            response (Response): The response object to query
            css_queries (List[str]): A list of CSS queries to test.
        Returns
            Optional[str]: The first successful CSS query, or None if none are successful.
        """
        for query in css_queries:
            if len(response.css(query)) > 0:
                return query
        return None

    def add_key(self, response: Response, loader: Loader, queries: List[str], key: str) -> None:
        """
        Add data to the loader based on the first successful CSS query
        Args:
            response (Response): The response object to query.
            loader (Loader): The loader to add data to.
            queries (List[str]): A list of CSS queries to try.
            key (str): The key to add to the loader.
        """
        potential_key = self.extractable_content(response, queries)
        if potential_key is not None:
            loader.add_css(key, potential_key)
        else:
            loader.add_value(key, "n/a")
