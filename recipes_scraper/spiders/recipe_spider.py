import scrapy
from sys import path
path.append('/Users/Yordy/recipes_scraper')
from recipes_scraper.items import RecipeScraperItem
from  scrapy.loader import  ItemLoader


class RecipeSpider(scrapy.Spider):
    name='recipe'
    start_urls= ['https://www.seriouseats.com/recipes-by-world-cuisine-5117277']

    def parse(self, response):
        links=response.css('a.comp.card::attr(href)').getall()
        for link in links:
            yield response.follow(link,callback=self.parse_recipe)

    def parse_recipe(self,response):

        for recipe in response.css('div.l-container.article__container'):

            l=ItemLoader(item= RecipeScraperItem(),selector=recipe)

            l.add_css('Recipe_Name', 'h1.heading__title')
            l.add_css('Ingredients','li.simple-list__item.js-checkbox-trigger.ingredient.text-passage')
            l.add_css('alt_ingredients','.structured-ingredients__list-item p')
            if (len(['Ingredients']) or len(['alt_ingredients']))>1 :
                yield l.load_item()


