from services.scrape.PriceScraper import PriceScraper
from services.scrape.AmazonScraper import AmazonScraper
from enum import Enum

class Marketplace(Enum):
    AMAZON = "https://www.amazon.com/"
    EBAY = "https://www.ebay.com/"
    ETSY = "https://www.etsy.com/"

class ScraperFactory:
    def __init__(self):
        self.scrapers = {
            Marketplace.AMAZON: AmazonScraper
        }

    def create_scraper(self, marketplace: Marketplace) -> PriceScraper:
        return self.scrapers[marketplace]()
