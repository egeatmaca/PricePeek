import os
from services.scrapers.ScraperFactory import ScraperFactory, Marketplace
from services.analyzers.PriceAnalyzer import PriceAnalyzer
import logging

class AnalysisController:
    def scrape_and_analyze(self, marketplace_str: str, search_query: str) -> None:
        marketplace = None
        if marketplace_str == "amazon":
            marketplace = Marketplace.AMAZON
        elif marketplace_str == "ebay":
            marketplace = Marketplace.EBAY
        elif marketplace_str == "etsy":
            marketplace = Marketplace.ETSY
        else:
            raise ValueError(f"Marketplace {marketplace_str} is not found.")


        print(f"Started scraping and analyzing {search_query} on {marketplace}...")
        logging.info(f"Started scraping and analyzing {search_query} on {marketplace}...")

        scraper = ScraperFactory().create_scraper(marketplace)
        product_infos = scraper.get_product_infos(search_query)

        analyzer = PriceAnalyzer()
        analysis = analyzer.analyze(product_infos)

        print(f"Finished scraping and analyzing {search_query} on {marketplace}")
        logging.info(f"Finished scraping and analyzing {search_query} on {marketplace}")

        return analysis



    

    
    
    
