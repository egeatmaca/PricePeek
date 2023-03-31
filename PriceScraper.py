from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os
from typing import Generator
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
from webdriver_manager.chrome import ChromeDriverManager


class MarketPlace(Enum):
    AMAZON = "https://www.amazon.com/"
    EBAY = "https://www.ebay.com/"
    BESTBUY = "https://www.bestbuy.com/"


class PriceScraper:
    def __init__(self, marketplace):
        self.marketplace = marketplace
        self.url = marketplace.value

    def get_options(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

        prefs = {}
        options.experimental_options["prefs"] = prefs
        prefs["profile.default_content_settings"] = {"images": 2}

        return options

    def create_driver(self):
        service = None
        if os.path.exists("/usr/local/bin/chromedriver"):
            service = ChromeService("/usr/local/bin/chromedriver")
        else:
            service = ChromeService(ChromeDriverManager().install())

        driver = webdriver.Chrome(service=service, options=self.get_options())

        return driver
    
    def get_search_links(self, search_query:str) -> Generator:
        driver = self.create_driver()
        wait = WebDriverWait(driver, 10)

        try:
            driver.get(self.url)

            search_bar = wait.until(
                ec.presence_of_element_located((By.ID, "twotabsearchtextbox")))
            
            search_bar.send_keys(search_query)
            search_bar.send_keys(Keys.RETURN)
            
            search_results = wait.until(
                ec.presence_of_all_elements_located((By.CSS_SELECTOR, "div.s-result-item a.a-link-normal")))
            
            for result in search_results:
                yield result.get_attribute("href")
        except Exception as e:
            print(e)
        finally:
            driver.quit()

    def get_price(self, link: str) -> float:
        driver = self.create_driver()
        wait = WebDriverWait(driver, 10)

        try:
            driver.get(link)

            price_whole = wait.until(
                ec.presence_of_element_located((By.CLASS_NAME, "a-price-whole")))
            
            price_fraction = wait.until(
                ec.presence_of_element_located((By.CLASS_NAME, "a-price-fraction")))
            
            price_symbol = wait.until(
                ec.presence_of_element_located((By.CLASS_NAME, "a-price-symbol")))
            
            value = float(price_whole.text.replace(',', '') + "." + price_fraction.text)
            currency = price_symbol.text
            price = {"value": value, "currency": currency}
            return price
        except Exception as e:
            print(e)
        finally:
            driver.quit()

    def get_prices(self, search_query: str) -> Generator:
        search_link_generator = self.get_search_links(search_query)
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for link in search_link_generator:
                future = executor.submit(self.get_price, link)
                futures.append(future)

            for future in futures:
                result = future.result()
                print('PRICE:', result)
                yield result

if __name__ == "__main__":
    scraper = PriceScraper(MarketPlace.AMAZON)
    search_query = "laptop"
    print([price for price in scraper.get_prices(search_query)])
