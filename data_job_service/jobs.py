import os
from multiprocessing import Process
from scrape.ScraperFactory import ScraperFactory, Marketplace
from analyze.PriceAnalyzer import PriceAnalyzer
import logging

def scrape_and_analyze(marketplace: Marketplace, search_query: str) -> None:
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



    

    
    
    
