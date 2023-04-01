import os
from scrape.ScraperFactory import ScraperFactory, Marketplace
from logs.log_config import config_logs

def test_scraper():
    scraper_factory = ScraperFactory()
    scraper = scraper_factory.create_scraper(Marketplace.AMAZON)
    product_infos = scraper.get_product_infos("iphone")

    for product_info in product_infos:
        print(product_info)

def test_scraper_pub():
    scraper_factory = ScraperFactory()
    scraper = scraper_factory.create_scraper(Marketplace.AMAZON)
    producer_config = {
        "bootstrap.servers": os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
    }
    scraper.publish_product_infos("iphone", producer_config)

if __name__ == "__main__":
    config_logs()

    test_scraper()

    

    
    
    
