from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from typing import Generator
from enum import Enum
from concurrent.futures import ThreadPoolExecutor

class MarketPlace(Enum):
    AMAZON = "https://www.amazon.com/"
    EBAY = "https://www.ebay.com/"
    BESTBUY = "https://www.bestbuy.com/"

class PriceScraper:
    def __init__(self, marketplace):
        self.marketplace = marketplace
        self.url = marketplace.value

    def get_options(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}

        return chrome_options

    def create_driver(self):
        # For local
        # service = ChromeService("chromedriver/chromedriver") 
        # driver = webdriver.Chrome(service=service)

        # For docker
        driver = webdriver.Chrome(options=self.get_options()) 

        return driver
    
    def get_search_links(self, search_query:str) -> Generator:
        driver = self.create_driver()

        driver.get(self.url)

        search_bar = driver.find_element(By.ID, "twotabsearchtextbox")
        search_bar.send_keys(search_query)
        search_bar.send_keys(Keys.RETURN)

        try:
            search_results = driver.find_elements(
                By.CSS_SELECTOR, "div.s-result-item a.a-link-normal")
            for result in search_results:
                yield result.get_attribute("href")
        except Exception as e:
            print(e)
        finally:
            driver.quit()

    def get_price(self, link: str) -> float:
        driver = self.create_driver()

        try:
            driver.get(link)
            price_whole = driver.find_element(
                By.CLASS_NAME, "a-price-whole")
            price_fraction = driver.find_element(
                By.CLASS_NAME, "a-price-fraction")
            price_symbol = driver.find_element(
                By.CLASS_NAME, "a-price-symbol")
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
        search_link_generator = list(search_link_generator)[4:10]
        
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
