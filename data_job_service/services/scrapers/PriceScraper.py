from abc import ABC, abstractmethod
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import json
from threading import Lock
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
from typing import Generator


class PriceScraper(ABC):
    def __init__(self):
        self.driver_file_lock = Lock()

    def get_options(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

        return options

    def create_driver(self):
        self.driver_file_lock.acquire(blocking=True)

        service = None
        if os.path.exists("/usr/local/bin/chromedriver"):
            service = Service("/usr/local/bin/chromedriver")
        else:
            service = Service(ChromeDriverManager().install())

        driver = uc.Chrome(service=service, options=self.get_options())

        self.driver_file_lock.release()

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

    def publish_product_infos(self, search_query: str, kafka_config: dict) -> None:
        topic_name = search_query.replace(' ', '_')

        kafka_admin = AdminClient(kafka_config)
        topics = kafka_admin.list_topics()
        if topic_name not in topics.topics:
            kafka_admin.create_topics([NewTopic(topic_name, 1, 1)])

        producer = Producer(**kafka_config)
        for product_info in self.get_product_infos(topic_name):
            product_info_bytes = json.dumps(product_info).encode('utf-8')
            producer.produce(topic_name, product_info_bytes)
            producer.flush()
            print(f'Published product info: {product_info}')
