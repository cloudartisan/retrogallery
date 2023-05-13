# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


import scrapy


class ImageItem(scrapy.Item):
    spider = scrapy.Field() # the name of the spider that scraped the image
    gallery_title = scrapy.Field()
    gallery_url = scrapy.Field()
    image_title = scrapy.Field()
    image_urls = scrapy.Field() # see settings.IMAGES_URLS_FIELD
    images = scrapy.Field() # see settings.IMAGES_RESULT_FIELD