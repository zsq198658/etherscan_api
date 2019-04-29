# /usr/bin/python3.7
# -----*.* coding='utf-8' *.*--------

import scrapy
from scrapy import Request
from ..items import MyEtherscanItem


class Scan_spider(scrapy.Spider):
        name = "scan"
        allowed_domains = ["etherscan.io"]
        start_urls = ['https://etherscan.io/tokens']

        def parse(self, response):
            scanItem = MyEtherscanItem()
            name_get = response.xpath('//a[@class="text-primary"]/text()').extract()
            address_get = response.xpath('//a[@class="text-primary"]/@href').extract()
            for i in range(len(name_get)):
                scanItem['name'] = name_get[i]
                scanItem['address'] = address_get[i][7:]
                yield scanItem
            next_page = response.xpath('//a[@aria-label="Next"]/@href').extract_first()
            if next_page:
                next_page = 'https://etherscan.io/' + next_page
                print(next_page)
                yield Request(next_page, callback=self.parse)

