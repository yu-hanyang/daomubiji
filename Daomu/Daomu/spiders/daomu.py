import scrapy
from ..items import DaomuItem
import os


class DaomuSpider(scrapy.Spider):
    name = 'daomu'
    allowed_domains = ['www.daomubiji.com']
    start_urls = ['https://www.daomubiji.com/']

    def parse(self, response):
        a_list = response.xpath('.//li[contains(@id,"menu-item-20")]/a')
        if not os.path.exists('./novel'):
            os.mkdir('./novel')
        for a in a_list:
            item = DaomuItem()
            parent_title = a.xpath('./text()').get()
            parent_url = a.xpath('./@href').get()
            directory = f'./novel/{parent_title}/'
            item['directory'] = directory
            if not os.path.exists(directory):
                os.mkdir(directory)
            yield scrapy.Request(url=parent_url,meta={'meta1':item},callback=self.parse_two_page)


    def parse_two_page(self, response):
        meta1 = response.meta['meta1']
        article_list = response.xpath('//article')
        for article in article_list:
            #新建一个DaonuItem
            item = DaomuItem()
            item['son_title'] = article.xpath('./a/text()').get()
            son_url = article.xpath('./a/@href').get()
            #这里如果不重新来个对象给item，会乱

            item['directory'] = meta1['directory']

            yield scrapy.Request(url=son_url,meta={'item':item},callback=self.parse_three_page)



    def parse_three_page(self, response):
        item = response.meta['item']
        content_list = response.xpath('//article[@class="article-content"]/p/text()').extract()
        item['content'] = '\n'.join(content_list)


        yield item
