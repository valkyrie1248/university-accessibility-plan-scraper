from scrapy.spiders import XMLFeedSpider


class SitemapSpider1Spider(XMLFeedSpider):
    name = "sitemap_spider1"
    allowed_domains = ["ssss.com"]
    start_urls = ["https://ssss.com"]
    iterator = "iternodes"  # you can change this; see the docs
    itertag = "item"  # change it accordingly

    def parse_node(self, response, selector):
        item = {}
        #item["url"] = selector.select("url").get()
        #item["name"] = selector.select("name").get()
        #item["description"] = selector.select("description").get()
        return item
