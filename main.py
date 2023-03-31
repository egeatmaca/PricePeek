from PriceScraper import PriceScraper
from Marketplace import Marketplace
from log_config import config_logs

if __name__ == "__main__":
    config_logs()

    scraper = PriceScraper(Marketplace.AMAZON)
    prices = scraper.get_prices("iphone")
    
    for price in prices:
        print(price)
