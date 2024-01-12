#!/bin/bash
exec poetry run scrapy crawl urls
exec poetry run scrapy crawl articles
