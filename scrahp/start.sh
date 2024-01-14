#!/bin/bash
set -e

poetry run scrapy crawl urls
exec poetry run scrapy crawl articles
