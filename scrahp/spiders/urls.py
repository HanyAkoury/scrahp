from pathlib import Path
import scrapy
from ..items import Url
from ..loaders import Loader


class UrlsSpider(scrapy.Spider):
    """
    Spider that can crawl the website and try to get the different articles from the website.
    The idea is to crawl and store the articles as well as their urls inside a json, that will serve
    as an url inputs to scrap for more information about the said articles.
    """

    custom_settings = {
        "ITEM_PIPELINES": {
            "scrahp.pipelines.UrlPipeline": 300,
            "scrahp.pipelines.JsonWriterPipeline": 400,
            "scrahp.pipelines.SQLitePipeline": 500,
        }
    }
    name = "urls"
    local_urls = []
    url = [
        "https://www.bbc.com/news",
    ]

    def start_requests(self):
        for url in self.url:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.save_page_offline(response=response)
        articles = response.css("a.gs-c-promo-heading")

        for article in articles:
            loader = Loader(item=Url(), selector=article)
            loader.add_css("title", "h3::text, span::text")
            loader.add_css("url", "a::attr(href)")
            yield loader.load_item()

    def save_page_offline(self, response) -> None:
        page = response.url.split("/")[-2]
        directory = "./pages/"
        filename = f"{directory}Articles2-{page}.html"

        # Create the directory if it doesn't exist
        Path(directory).mkdir(parents=True, exist_ok=True)

        with open(filename, "wb") as file:
            file.write(response.body)

        self.local_urls.append(filename)
        self.log(f"Saved file {filename}")
