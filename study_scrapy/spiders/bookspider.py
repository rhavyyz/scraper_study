import scrapy
from study_scrapy.items import BookItem 

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
      yield response.follow(next_page, self.parse)