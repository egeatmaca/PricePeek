from abc import ABC, abstractmethod
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
from typing import Generator
from confluent_kafka import Producer


class PriceScraper(ABC):

    def get_options(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

        return options

    def create_driver(self):
        service = None
        if os.path.exists("/usr/local/bin/chromedriver"):
            service = Service("/usr/local/bin/chromedriver")
        else:
            service = Service(ChromeDriverManager().install())

        driver = uc.Chrome(service=service, options=self.get_options())

        return driver

    @abstractmethod
    def get_search_links(self, search_query: str) -> Generator:
        pass

    @abstractmethod
    def get_product_info(self, link: str) -> dict:
        pass

    @abstractmethod
    def get_product_infos(self, search_query: str) -> Generator:
        pass

    def publish_product_infos(self, search_query: str, producer_config: dict) -> None:
        producer = Producer(producer_config)
        for product_info in self.get_product_infos(search_query):
            producer.produce(search_query, product_info)
            producer.flush()