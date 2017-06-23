import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://www.jianshu.com/p/e9b0382c52ba'
    ]

    def parse(self, response):
        page = response.url.split("/")[-1]
        filename = 'html/%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)