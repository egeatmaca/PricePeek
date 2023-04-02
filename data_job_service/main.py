import os
from scrape.ScraperFactory import ScraperFactory, Marketplace
from analyze.PriceAnalyzer import PriceAnalyzer
from logs.log_config import config_logs
import logging
import time
from concurrent.futures import ThreadPoolExecutor

def run_scraper():
    scraper_factory = ScraperFactory()
    scraper = scraper_factory.create_scraper(Marketplace.AMAZON)
    product_infos = scraper.get_product_infos("iphone")

    for product_info in product_infos:
        print(product_info)

def run_scraper_pub():
    scraper_factory = ScraperFactory()
    scraper = scraper_factory.create_scraper(Marketplace.AMAZON)
    kafka_config = {
        "bootstrap.servers": os.environ.get("KAFKA_BROKER")
    }
    logging.info(f"Kafka config: {kafka_config}")
    scraper.publish_product_infos("iphone", kafka_config)


def run_scraper_analyzer_pubsub():
    search_query = "iphone"

    scraper = ScraperFactory().create_scraper(Marketplace.AMAZON)
    kafka_broker = os.environ.get("KAFKA_BROKER")
    kafka_config = {"bootstrap.servers": kafka_broker}

    analyzer = PriceAnalyzer()
    spark_master = os.environ.get("SPARK_MASTER")

    with ThreadPoolExecutor(max_workers=2) as executor:
        scrape_thread = executor.submit(scraper.publish_product_infos, search_query, kafka_config)
        analyze_thread = executor.submit(analyzer.consume_product_infos, search_query, kafka_broker, spark_master)

        scrape_thread.result()
        analyze_thread.result()


if __name__ == "__main__":
    time.sleep(30)
    config_logs()
    run_scraper_pub()

    

    
    
    
