# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class StudyScrapySpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class StudyScrapyDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

from urllib.parse import urlencode
from random import randint
import requests
from scrapy.http import Headers


class FakeUserAgentMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    
    def __request_headers(self):
        headers = {'api_key' : self.key, 'num_results' : self.result_number}
        response = requests.get(self.url, params=urlencode(headers))
        self.headers = response.json().get('result', [])


    def __init__(self, settings) -> None:
        self.key = settings.get('SCRAPEOPS_API_KEY')
        self.url = settings.get('SCRAPEOPS_API_URL')
        self.result_number = settings.get('SCRAPEOPS_RESULT_NUMBER')
        self.headers = []

        self.__request_headers()

    def __random_header(self):
        return self.headers[randint(0, len(self.headers)-1)]
    
    def process_request(self, request, spider):
        request.headers = Headers(self.__random_header())

import base64

class ProxyServerMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    
    def __init__(self, settings) -> None:
        self.url = settings.get('PROXY_SERVER_URL')
        self.user = settings.get('PROXY_USERNAME')
        self.password = settings.get('PROXY_PASSWORD')
        self.port = settings.get('PROXY_PORT')

    def process_request(self, request, spider):
        credentials = f'{self.user}:{self.password}'
        basic_authentication = 'Basic ' + base64.b64encode(credentials.encode()).decode()
        host = f'https://{self.url}:{self.port}'

        request.meta['proxy'] = host
        request.headers['Proxy-Authorization'] = basic_authentication
