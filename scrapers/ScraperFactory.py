from scrapers.PriceScraper import PriceScraper
from scrapers.AmazonScraper import AmazonScraper
from scrapers.Marketplace import Marketplace

class ScraperFactory:
    def __init__(self):
        self.scrapers = {
            Marketplace.AMAZON: AmazonScraper
        }

    def create_scraper(self, marketplace: Marketplace) -> PriceScraper:
        return self.scrapers[marketplace]()
