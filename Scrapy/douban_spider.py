# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem

class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/top250']

    #default parse method
    def parse(self, response):
        
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        
        for i_item in movie_list:
        	#import item file
        	douban_item = DoubanItem()
        	# parse data
        	douban_item['serial_number'] = i_item.xpath(".//div[@class='item']//em/text()").extract_first()
        	douban_item['movie_name'] = i_item.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()
        	content = i_item.xpath(".//div[@class='info']/div[@class='bd']/p[1]/text()").extract()
        	# parse multirow data
        	for i_cont in content:
        		content_s = "".join(i_cont.split())
        		douban_item['intro'] = content_s
        	douban_item['star'] = i_item.xpath(".//span[@class='rating_num']/text()").extract_first()
        	douban_item['review'] = i_item.xpath(".//div[@class='star']//span[4]/text()").extract_first()
        	douban_item['cont'] = i_item.xpath(".//p[@class='quote']/span/text()").extract_first()
        	
        	# yield to pipelines
        	yield douban_item

        #parse next page
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        if next_link:
        	next_link = next_link[0]
        	yield scrapy.Request("https://movie.douban.com/top250"+next_link, callback = self.parse)

        	
