import time
from scrapy.linkextractors import LinkExtractor

from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver

from spider.items import ArticleItem


class QuotesSpider(CrawlSpider):
    name = "quotes"

    # 专题页
    topic_url = 'http://www.jianshu.com/recommendations/collections?utm_medium=index-collections&utm_source=desktop'

    allowed_domains = ["jianshu.com"]

    start_urls = []

    # 定义爬取URL的规则，并指定回调函数为parse_item
    rules = [
        # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
        Rule(LinkExtractor(allow=(r'http://www.jianshu.com/p/[a-z0-9]+[^?]$')), callback="parse_item", follow=False)
    ]

    def __init__(self):
        CrawlSpider.__init__(self)
        # use any browser you wish
        self.browser = webdriver.Firefox()

        self.browser.get(self.topic_url)
        more_btn = self.browser.find_element_by_class_name('load-more-btn')
        while more_btn is not None:
            if more_btn.value_of_css_property('display') == 'none':
                break
            more_btn.click()
            time.sleep(2)
            more_btn = self.browser.find_element_by_class_name('load-more-btn')

        cards = self.browser.find_elements_by_class_name('avatar-collection')
        for card in cards:
            url = card.get_attribute('href')
            self.start_urls.append(url)

    def __del__(self):
        pass
        # self.browser.close()

    def parse_item(self, response):
        item = ArticleItem()
        item['url'] = response.url
        for article in response.css('div.article'):
            item['title'] = article.css('h1.title::text').extract_first()

        for info in response.css('div.author div.info'):
            item['author'] =info.css('span.name a::text').extract_first()
            item['date'] = info.css('div.meta span.publish-time::text').extract_first()
        return item