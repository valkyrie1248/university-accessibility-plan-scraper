from scrapy_demo.spiders import h1_spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl()
    process.start()


if __name__ == '__main__':
    main()