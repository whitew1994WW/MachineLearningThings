import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from goodfood.items import RecipeItem

class scraper(CrawlSpider):
    name = 'scraper'
    allowed_domains = ['bbcgoodfood.com']
    start_urls = ['https://www.bbcgoodfood.com/recipes/764647/sausage-and-bean-onepot']
    count = 0
    rules = (
        Rule(LinkExtractor(allow=(r'https://www.bbcgoodfood.com/recipes/\d*/.*$')), callback='parse_item'),
        Rule(LinkExtractor(allow=(r'https://www.bbcgoodfood.com/recipes/.*'))),
    )

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        item = RecipeItem()
        item['ingredients'] = response.xpath(r'//*[@id="recipe-ingredients"]//li').extract()#.re_first(r'content="([\w\s]*)">')
        item['method'] = response.xpath(r'//*[@id="recipe-method"]/div/ol/li').extract()
        item['nutrition'] = response.xpath(r'//*[@id="recipe-header-more-info"]/div/div[2]/ul').extract()
        item['title'] = response.css(".recipe-header__title").extract()
        item['rating'] = response.css(".recipe-header__rating").extract()
        item['prep_time'] = response.css(".recipe-details__cooking-time-prep").extract()
        item['cook_time'] = response.css(".recipe-details__cooking-time-cook").extract()
        item['skill'] = response.css(".recipe-details__item--skill-level").extract()
        item['servings'] = response.css(".recipe-details__item--servings").extract()
        return item