import scrapy
from datetime import datetime
from scrapy.spiders import SitemapSpider

domain = input("What domain should we crawl? ")
starting_urls = input("Give us the url that you want us start crawling from: ")

class SitemapSpider2Spider(SitemapSpider):
    name = "sitemapspider2_spider"
    allowed_domains = [domain]
    sitemap_urls = [starting_urls]
    sitemap_alternate_links: bool = True
    namespaces = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    def sitemap_filter(self, entries):
        for entry in entries:
            date_time = datetime.strptime(entry["lastmod"], "%Y-%m-%d")
            if date_time.year >= 2023:
                yield entry

    def parse_sitemap(self, response):  #now what do I do with these?
        urls = response.xpath('//sitemap:loc/text()', namespaces=namespaces).getall()
        for url in urls:
            yield url
        
