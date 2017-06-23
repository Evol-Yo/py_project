import logging

import scrapy
import time

import sys
from scrapy.spiders import CrawlSpider, Spider
from selenium import webdriver

from jianshu_spider.items import ArticleItem


logging.basicConfig(level=logging.INFO, filename='log.log', filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

class JianShuSpider(scrapy.Spider):
    name = "jianshu"

    # entrance_url = 'http://www.jianshu.com/recommendations/collections?order_by=hot'

    start_urls = []

    allowed_domains = ["jianshu.com"]

    # def __init__(self):
    #     Spider.__init__(self)
    #     self.browser = webdriver.Firefox()
    #     self.browser.get(self.entrance_url)
    #
    #     topic_urls = []
    #
    #     more_btn = self.browser.find_element_by_class_name('load-more-btn')
    #     while more_btn is not None:
    #         if more_btn.value_of_css_property('display') == 'none':
    #             break
    #         more_btn.click()
    #         time.sleep(2)
    #         more_btn = self.browser.find_element_by_class_name('load-more-btn')
    #
    #     cards = self.browser.find_elements_by_class_name('avatar-collection')
    #
    #     topic_count = 0
    #     article_count = 0
    #
    #     for card in cards:
    #         url = card.get_attribute('href')
    #         topic_count += 1
    #         logging.info("#### topic: " + str(topic_count) + '\t' + url + '?order_by=top')
    #
    #         topic_urls.append(url + '?order_by=top')
    #
    #
    #     for topic_url in topic_urls:
    #         self.browser.get(topic_url)
    #         count = 50
    #         while count > 0:
    #             count -= 1
    #             self.browser.execute_script('window.scrollBy(0, 10000)')
    #             time.sleep(1)
    #
    #         note_list = self.browser.find_element_by_class_name('note-list')
    #         titles = note_list.find_elements_by_class_name('title')
    #         for title in titles:
    #             try:
    #                 article_url = title.get_attribute('href')
    #             except Exception:
    #                 logging.info("Error: " + str(title))
    #                 continue
    #             if(article_url is None):
    #                 continue
    #             article_count += 1
    #             logging.info("#### article: " + str(article_count) + '\t'  + article_url)
    #
    #             self.start_urls.append(article_url)

    def __init__(self):
        Spider.__init__(self)
        with open('/home/yuxiang/py_project/log.log') as log:
            for line in log:
                if (line.startswith('INFO:root:#### article')):
                    url = line[line.index('http'):-1]
                    print(url)
                    self.start_urls.append(url)



    def parse(self, response):
        page = response.url.split("/")[-1]
        print(page)
        filename = 'html/%s.html' % page
        with open(filename, 'w') as f:
            f.write(response.body.decode('utf-8'))

        item = ArticleItem()
        item['url'] = response.url
        for article in response.css('div.article'):
            item['title'] = article.css('h1.title::text').extract_first()

        for info in response.css('div.author div.info'):
            item['author'] =info.css('span.name a::text').extract_first()
            item['date'] = info.css('div.meta span.publish-time::text').extract_first()
        return item