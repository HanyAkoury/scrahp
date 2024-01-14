#

import re
from pathlib import Path
from typing import Any, List

import scrapy
from scrapy.http import Response
from scrapy.selector import SelectorList

from scrahp.items import Url
from scrahp.loaders import Loader


class UrlsSpider(scrapy.Spider):
    """
    Spider for crawling a website and extracting article URLs.

    This spider crawls specified URLs and extracts article information, such as titles
    and URLs, storing them for further processing. It is designed to gather URLs that
    will serve as inputs for scraping more detailed information about the articles.
    """

    custom_settings = {
        "ITEM_PIPELINES": {
            "scrahp.pipelines.UrlPipeline": 300,
            "scrahp.pipelines.JsonWriterPipeline": 400,
        }
    }
    name: str = "urls"
    local_urls: List[str] = []
    urls: List[str] = [
        # 'https://www.bbc.com/',
        "https://www.bbc.com/news",
        # "https://www.bbc.com/sport",
        # 'https://www.bbc.com/future/earth',
        # 'https://www.bbc.com/reel',
        # 'https://www.bbc.com/worklife',
        # 'https://www.bbc.com/travel',
        # 'https://www.bbc.com/culture',
        # 'https://www.bbc.com/future'
    ]

    def start_requests(self) -> Any:
        """
        Generates Scrapy Requests from the list of URLs to be crawled.
        """
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: Response, **kwargs: Any) -> Any:
        """
        Parse the response and extract article URLs and titles.

        Args:
            response (Response): The response object to parse.

        Yields:
            Item: The extracted URL item.
        """
        self.save_page_offline(response=response)
        available_urls: SelectorList = response.css("a.gs-c-promo-heading")

        for url in available_urls:
            url_loader: Loader = Loader(item=Url(), selector=url)
            url_loader.add_css("title", "h3::text, span::text")
            url_loader.add_value("base_url", self.extract_base_url(response))
            url_loader.add_css("url", "a::attr(href)")
            yield url_loader.load_item()

    def save_page_offline(self, response: Response) -> None:
        """
        Save a copy of the crawled page for offline analysis and eventual backup.

        Args:
            response (Response): The response object to save.
        """
        page = response.url.split("/")[-2]
        directory = "./pages/"
        filename = f"{directory}Articles2-{page}.html"

        # Create the directory if it doesn't exist
        Path(directory).mkdir(parents=True, exist_ok=True)

        with open(filename, "wb") as file:
            file.write(response.body)

        self.local_urls.append(filename)
        self.log(f"Saved file {filename}")

    def extract_base_url(self, response: Response) -> str:
        """
        Extract the base URL from the response object because it's needed futher in the process.

        Args:
            response (Response): The response object to extract the base URL from.

        Returns:
            str: The extracted base URL, or 'n/a' if not found.
        """
        base_url = re.search(r"(https?://[^/]+)", response.request.url)
        if base_url is not None:
            return base_url.group(1)
        return "n/a"
