import scrapy


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

    number = 0

    def parse(self, response):
      books = response.css('article.product_pod')
      for book in books:

        self.number = self.number + 1

        yield {
             'title': book.css('h3 a::attr(title)').get(),
             'url': book.css('h3 a::attr(href)').get(),             
             'id': self.number ,

             'price': book.css('.product_price .price_color::text').get() 
          }

      next_page = response.css('li.next a ::attr(href)').get()

      if next_page is None:
        return

      if 'catalogue/' not in next_page:
        next_page = "catalogue/" + next_page

      next_page = 'https://books.toscrape.com/' + next_page
      yield response.follow(next_page, self.parse)