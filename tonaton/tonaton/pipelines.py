# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pyrebase

config = {
    "apiKey": "AIzaSyAnFB3HxZlxwCVwPn0br2Gb0JqDYR7OnjU",
    "authDomain": "surreal-159622.firebaseapp.com",
    "databaseURL": "https://surreal-159622.firebaseio.com",
    "projectId": "surreal-159622",
    "storageBucket": "surreal-159622.appspot.com",
    "messagingSenderId": "213701187584"
}


class TonatonPipeline(object):
    def open_spider(self, spider):
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    def process_item(self, item, spider):
        self.db.child("apartments").push(dict(item))
        return item


from scrapy.exceptions import DropItem
import re

class DatePipeline(object):
    def process_item(self, item, spider):

        regexp = re.compile(r'Nov|Dec')
        if regexp.search(item['date']):
            return item
        else:
            raise DropItem("Is older than 60 days: %s" % item)




