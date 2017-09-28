import scrapy


class ShiyanlouCoursesSpider(scrapy.Spider):

    name = 'shiyanlou-githubs'

    @property
    def start_urls(self):

        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return(url_tmpl.format(i) for i in range(1, 5))

    def parse(self, response):
        for github in response.xpath('.//li[contains(@class,"col-12 d-block width-full py-4 border-bottom public source")]'):
            yield {
                'name': github.xpath('.//a[contains(@itemprop,"name codeRepository")]/text()[1]').extract_first().strip(),
                'update_time': github.xpath('.//div[@class="f6 text-gray mt-2"]/relative-time/@datetime').extract_first()
            }
