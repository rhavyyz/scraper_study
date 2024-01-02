from typing import Iterable
import scrapy
from scrapy.http import Request
from study_scrapy.items import BookItem 
from random import randint

class BookspiderSpider(scrapy.Spider):
    # The name we reference 
    name = "bookspider"

    '''
      Spiders can crawl through multiple links "recursively"
      and setting the domains you want this to be permited prevents
      your spider to crawl out of the webpages you want
    '''
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]


    '''
      custom_settings override settings from settings.py
      in this specific spider
    '''
    custom_settings = {
      'FEED': {
        'bookdata.json': {
                          'format' : 'json',
                          'override' : True
                         }
      }
    }

    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
    ]

    def random_user_agent(self):
      return {'User-Agent': self.user_agent_list[randint(0, len(self.user_agent_list) - 1)]}

    def start_requests(self) -> Iterable[Request]:
      for url in self.start_urls:
        yield scrapy.Request(url, self.parse, headers= self.random_user_agent())

    def parse_book_page(self, response):

      main = response.css('div.product_main')[0]

      item = BookItem()
      
      item['title'] = main.css('h1::text').get()
      item['description'] = response.xpath('//div[@id=\'product_description\']/following-sibling::p/text()').get()
      item['price'] = main.css('p.price_color::text').get()
      item['in_stock'] = 'In stock' in response.xpath('//table/tr[6]/td/text()').get()
      item['book_url'] = response.request.url
      item['stars'] = main.css("p.star-rating ::attr(class)").get().split()[1]
      item['category']: response.xpath('//ul[@class=\'breadcrumb\']/li[@class=\'active\']/preceding-sibling::li[1]/a/text()').get()
      
      yield item

    def parse(self, response):
      books = response.css('article.product_pod')
      for book in books:
        next_page = book.css('h3 a ::attr(href)').get()
        
        if 'catalogue/' not in next_page:
          next_page = "catalogue/" + next_page

        next_page = self.start_urls[0] + next_page
 
        yield response.follow(next_page, self.parse_book_page)

      next_page = response.css('li.next a ::attr(href)').get()

      if next_page is None:
        return

      if 'catalogue/' not in next_page:
        next_page = "catalogue/" + next_page

      next_page = self.start_urls[0] + next_page
      yield response.follow(next_page, self.parse, headers= self.random_user_agent())