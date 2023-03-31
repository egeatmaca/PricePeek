from services.scrape.ScraperFactory import ScraperFactory, Marketplace
from logs.log_config import config_logs

if __name__ == "__main__":
    config_logs()

    scraper_factory = ScraperFactory()
    scraper = scraper_factory.create_scraper(Marketplace.AMAZON)
    product_infos = scraper.get_product_infos("iphone")
    
    for product_info in product_infos:
        print(product_info)
