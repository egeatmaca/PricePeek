from abc import ABC, abstractmethod
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
from threading import Lock
from typing import Generator
import logging


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
        
        driver = None
        try:
            service = None
            if os.path.exists("/usr/local/bin/chromedriver"):
                service = Service("/usr/local/bin/chromedriver")
            else:
                service = Service(ChromeDriverManager().install())

            driver = uc.Chrome(service=service, options=self.get_options())
        except Exception as e:
            print(f"Error creating driver: {e}")
            logging.error(f"Error creating driver: {e}")
        finally:
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

