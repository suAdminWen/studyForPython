# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from scrapy.http import HtmlResponse
from logging import getLogger
import time


class CasSpiderSpiderMiddleware(object):
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

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CasSpiderDownloaderMiddleware(object):
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
        spider.logger.info('Spider opened: %s' % spider.name)


class SeleniumMiddleware():
    # 经常需要在pipeline或者中间件中获取settings的属性，可以通过scrapy.crawler.Crawler.settings属性
    @classmethod
    def from_crawler(cls, crawler):
        # 从settings.py中，提取selenium设置参数，初始化类
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                   isLoadImage=crawler.settings.get('LOAD_IMAGE'),
                   windowHeight=crawler.settings.get('WINDOW_HEIGHT'),
                   windowWidth=crawler.settings.get('WINDOW_WIDTH')
                   )

    def __init__(self, timeout=30, isLoadImage=True, windowHeight=None, windowWidth=None):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        self.isLoadImage = isLoadImage
        # 定义一个属于这个类的browser，防止每次请求页面时，都会打开一个新的chrome浏览器
        # 这样，这个类处理的Request都可以只用这一个browser
        self.browser = webdriver.Chrome()
        if windowHeight and windowWidth:
            self.browser.set_window_size(900, 900)
        self.browser.set_page_load_timeout(self.timeout)        # 页面加载超时时间
        self.wait = WebDriverWait(self.browser, 25)             # 指定元素加载超时时间

        def process_request(self, request, spider):
            '''
            用chrome抓取页面
            :param request: Request请求对象
            :param spider: Spider对象
            :return: HtmlResponse响应
            '''
            # self.logger.debug('chrome is getting page')
            print(f"chrome is getting page")
            # 依靠meta中的标记，来决定是否需要使用selenium来爬取
            usedSelenium = request.meta.get('usedSelenium', False)
            if usedSelenium:
                try:
                    print('=============================')
                    print(request.url)

                    self.browser.get(request.url)
                    time.sleep(2)
                except Exception as e:
                    # self.logger.debug(f'chrome getting page error, Exception = {e}')
                    print(f"chrome getting page error, Exception = {e}")
                    return HtmlResponse(url=request.url, status=500, request=request)
                else:
                    time.sleep(3)
                    return HtmlResponse(url=request.url,
                                        body=self.browser.page_source,
                                        request=request,
                                        # 最好根据网页的具体编码而定
                                        encoding='utf-8',
                                        status=200)
