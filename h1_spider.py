import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

'''
Goal of this spider is to get enough info to potentially find a path to the page that will cover digital accessibility.
'''

domain = input("What domain should we crawl? ")
starting_url = input("Give us the url that you want us start crawling from: ")

class H1SpiderSpider(CrawlSpider):
    name = "h1_spider"
    allowed_domains = [domain]
    start_urls = [starting_url]
    
    custom_settings = {
		#'FEEDS': {'data/%(name)s/%(name)s_%(time)s.csv': { 'format': 'csv',}},
        'DEPTH_LIMIT' : '2'
		}

    rules = (Rule(LinkExtractor(), callback="parse_item", follow=True),)

    def parse_item(self, response):
        links = response.css('a::attr(href)').getall()
        items1 = response.xpath('//h1/text()').getall()
        items2 = response.xpath('//h2/text()').getall()
        #item = {}
        #item["domain_id"] = response.xpath('//input[@id="sid"]/@value').get()
        #item["name"] = response.xpath('//div[@id="name"]').get()
        #item["description"] = response.xpath('//div[@id="description"]').get()
        '''for l in links:
            yield{
                'link': l,
                'page': response.url
            }'''
        for i in items1:
            yield {
                'text' : i,
                'page' : response.url
            }
        for j in items2:
            yield {
                'text' : j,
                'page' : response.url
            }
