# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import ShiyanlougithubItem


class GithubsSpider(scrapy.Spider):
    name = 'githubs'

    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return(url_tmpl.format(i) for i in range(1, 5))

    def parse(self, response):
        for github in response.xpath('.//li[contains(@itemprop,"owns")]'):
            item = ShiyanlougithubItem()
            item['name'] = github.xpath('.//a[contains(@itemprop,"name codeRepository")]/text()[1]').extract_first().strip(),
            item['update_time'] = github.xpath('.//div[@class="f6 text-gray mt-2"]/relative-time/@datetime').extract_first()
            github_url = response.urljoin(github.xpath('.//div[@class="d-inline-block mb-1"]/h3/a/@href').extract_first())
            request = scrapy.Request(github_url, callback=self.parse_detail)
            request.meta['item'] = item
            yield request


    def parse_detail(self,response):
        item = response.meta['item']
        try:
            item['commits'] = response.xpath('//span[@class="num text-emphasized"]/text()').extract()[0].strip()
            item['branches'] = response.xpath('//span[@class="num text-emphasized"]/text()').extract()[1].strip()
            item['releases'] = response.xpath('//span[@class="num text-emphasized"]/text()').extract()[2].strip()
        except IndexError:
            item['commits'] = 0
            item['branches'] = 0
            item['releases'] = 0
        yield item

