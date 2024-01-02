# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


'''
    This serializer thing is usefull to small amount of data
    in case you dont want to write a lot of code and need fast development 
'''
def uppercase(value : str) -> str:
    return value.upper()

class BookItem(scrapy.Item):
    title = scrapy.Field() #(serializer = uppercase)
    description = scrapy.Field()
    price = scrapy.Field()
    in_stock = scrapy.Field()
    book_url = scrapy.Field()
    stars = scrapy.Field()
    category = scrapy.Field()
      