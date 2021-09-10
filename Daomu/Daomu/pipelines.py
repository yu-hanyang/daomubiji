# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymysql


class DaomuPipeline:
    def process_item(self, item, spider):
        filename = '{}{}.txt'.format(item['directory'],item['son_title'].replace(' ','_'))
        print(filename)
        with open(filename,mode='w+') as f:
            f.write(item['content'])
        return item
