import scrapy
from sys import path
from recipes_scraper.items import RecipeScraperItem
from scrapy.loader import ItemLoader

path.append('//Yordy/recipes_scraper')


class RecipeSpider(scrapy.Spider):

    name = 'recipe'
    start_urls = [
        'https://www.seriouseats.com/recipes-by-world-cuisine-5117277'
    ]

    def parse(self, response):
        links = response.css('a.comp.card::attr(href)').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_recipe)

        raw_image_urls = response.css('.image img ::attr(data-src)').getall()
        clean_image_urls = []
        for img_url in raw_image_urls:
            clean_image_urls.append(response.urljoin(img_url))

            yield {
                'image_urls': clean_image_urls
            }

    def parse_recipe(self, response):

        for recipe in response.css('div.l-container.article__container'):

            itemLoader = ItemLoader(item=RecipeScraperItem(),
                                    selector=recipe)

            itemLoader.add_css('Recipe_Name', 'h1.heading__title')
            itemLoader.add_css('Ingredients', "li.simple-list__item."
                               "js-checkbox-trigger.ingredient.text-passage")
            itemLoader.add_css('Ingredients',
                               '.structured-ingredients__list-item p')
            itemLoader.add_value('URL', response.url)
            if ['Ingredients'] is not None:
                yield itemLoader.load_item()
