# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import  TakeFirst,MapCompose,Join
from w3lib.html import remove_tags
import re

def remove_SpecialChars(char):
    return char.replace('\n', '')

#def remove_emptyString(char):
    #return char.remove("")

def remove_wierdchar(alt_char):
    if alt_char:
        alt_char=[re.sub(r'\<[^>]*\>','',char) for char in alt_char]
    return alt_char

class RecipeScraperItem(scrapy.Item):
    # define the fields for your item here like:
    Recipe_Name = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    Ingredients= scrapy.Field(input_processor=MapCompose(remove_tags,remove_SpecialChars),output_processor =Join())
    Ingredients=scrapy.Field(input_proccessor=MapCompose(remove_tags), output_processor= remove_wierdchar)
    URL = scrapy.Field(input_proccessor=MapCompose(remove_tags), output_processor=TakeFirst())

class RecipeImgItem(scrapy.Item):
    Img=scrapy.Field()