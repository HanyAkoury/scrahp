# import pdb
import re
from pathlib import Path
from typing import Any, List

import pdb
import scrapy
from scrapy.http import Response
from scrapy.selector import SelectorList

from scrahp.items import Url
from scrahp.loaders import Loader


class UrlsSpider(scrapy.Spider):
    """
    Spider that can crawl the website and try to get the different articles from the website.
    The idea is to crawl and store the articles as well as their urls inside a json, that will serve
    as an url inputs to scrap for more information about the said articles.
    """

    custom_settings = {
        "ITEM_PIPELINES": {
            "scrahp.pipelines.UrlPipeline": 300,
            "scrahp.pipelines.JsonUrlWriterPipeline": 400,
            "scrahp.pipelines.SQLitePipeline": 500,
        }
    }
    name = "urls"
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
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: Response, **kwargs: Any) -> Any:
        self.save_page_offline(response=response)
        available_urls: SelectorList = response.css("a.gs-c-promo-heading")

        for url in available_urls:
            url_loader: Loader = Loader(item=Url(), selector=url)
            url_loader.add_css("title", "h3::text, span::text")
            url_loader.add_value("base_url", self.extract_base_url(response))
            url_loader.add_css("url", "a::attr(href)")
            yield url_loader.load_item()

    def save_page_offline(self, response: Response) -> None:
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
        # pdb.set_trace()
        base_url = re.search(r"(https?://[^/]+)", response.request.url)
        if base_url is not None:
            return base_url.group(1)
        return "n/a"
