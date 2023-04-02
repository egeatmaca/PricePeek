import os
from concurrent.futures import ThreadPoolExecutor
from scrape.ScraperFactory import ScraperFactory, Marketplace
from analyze.PriceAnalyzer import PriceAnalyzer

def scrape_and_analyze(marketplace, search_query):
    marketplace_enum = None
    if marketplace == "amazon":
        marketplace_enum = Marketplace.AMAZON
    elif marketplace == "ebay":
        marketplace_enum = Marketplace.EBAY
    elif marketplace == "etsy":
        marketplace_enum = Marketplace.ETSY
    else:
        raise Exception("Marketplace not supported")

    scraper = ScraperFactory().create_scraper(marketplace_enum)
    kafka_broker = os.environ.get("KAFKA_BROKER")
    kafka_config = {"bootstrap.servers": kafka_broker}

    analyzer = PriceAnalyzer()
    spark_master = os.environ.get("SPARK_MASTER")

    with ThreadPoolExecutor(max_workers=2) as executor:
        scrape_thread = executor.submit(
            scraper.publish_product_infos, search_query, kafka_config)
        # analyze_thread = executor.submit(analyzer.consume_product_infos, search_query, kafka_broker, spark_master)

        scrape_thread.result()
        # analyze_thread.result()



    

    
    
    
