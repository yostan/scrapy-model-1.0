# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class templateItem(Item):
    # define the fields for your item here like:
    #if download image, Required
    image_urls = Field()
    images = Field()
    image_paths = Field()

