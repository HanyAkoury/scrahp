# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os
import pdb
import re
import sqlite3
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrahpPipeline:
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
        base_url = re.search(r'(https?://[^/]+)', spider.urls[-1]).group(1)
        return f"{base_url}{item['url'][-1]}"

class JsonWriterPipeline:
    def open_spider(self, spider):

        if not os.path.exists('data'):
            os.makedirs('data')

        self.file = open("./data/articles.json", "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        print("---")
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item
    

class SQLitePipeline:
    def __init__(self):
        self.db_file = 'db/scrahp.db'
    
    
    def open_spider(self, spider):
        try:
            # Connect to the SQLite database
            self.conn = sqlite3.connect(self.db_file)
            self.c = self.conn.cursor()
        except sqlite3.OperationalError:
            print(f"Database file '{self.db_file}' does not exist. Skipping database operations.")


    def close_spider(self, spider):
        if hasattr(self, 'conn'):
            # Commit the changes and close the connection
            self.conn.commit()
            self.conn.close()


    def process_item(self, item, spider):
        if not hasattr(self, 'conn'):
            return item

        # Insert the article into the database, ignoring duplicates based on the URL
        self.c.execute('''
            INSERT OR IGNORE INTO articles (title, url)
            VALUES (?, ?)
        ''', (item['title'], item['url']))

        return item
