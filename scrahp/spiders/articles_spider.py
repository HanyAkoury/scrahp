from pathlib import Path
import scrapy
import pdb
from ..articles import Article
from ..articles_loaders import ArticleLoader

class ArticlesSpider(scrapy.Spider):
    name = "articles"
    local_urls = []
    urls = [
        "https://www.bbc.com/news",
    ]

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        
        self.save_page_offline(response=response)
        articles = response.css('a.gs-c-promo-heading')
        
        for article in articles:
            loader = ArticleLoader(item=Article(), selector=article)
            loader.add_css('title', 'h3::text, span::text')
            loader.add_css('url', 'a::attr(href)')
            yield loader.load_item()

    def save_page_offline(self, response)-> None: 
        page = response.url.split("/")[-2]
        filename = f"./pages/Articles2-{page}.html"
        Path(filename).write_bytes(response.body)
        self.local_urls.append(filename)
        self.log(f"Saved file {filename}")