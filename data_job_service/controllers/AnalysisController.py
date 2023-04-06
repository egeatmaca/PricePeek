import os
from multiprocessing import Process
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
        kafka_broker = os.environ.get("KAFKA_BROKER")
        kafka_config = {"bootstrap.servers": kafka_broker}

        analyzer = PriceAnalyzer()
        spark_master = os.environ.get("SPARK_MASTER")

        scrape_process = Process(target=scraper.publish_product_infos, args=(search_query, kafka_config))
        analyze_process = Process(target=analyzer.consume_product_infos, args=(search_query, kafka_broker, spark_master))

        scrape_process.start()
        analyze_process.start()

        scrape_process.join()
        analyze_process.join()

        print(f"Finished scraping and analyzing {search_query} on {marketplace}")
        logging.info(f"Finished scraping and analyzing {search_query} on {marketplace}")

        return {"message": f"Finished scraping and analyzing {search_query} on {marketplace}"}



    

    
    
    
