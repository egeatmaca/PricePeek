from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from typing import Generator
from concurrent.futures import ThreadPoolExecutor
import logging
from services.scrapers.PriceScraper import PriceScraper

class AmazonScraper(PriceScraper):
    URL = "https://www.amazon.com/"
    ERROR_LIMIT = 5
    
    def get_search_links(self, search_query:str) -> Generator:
        driver = self.create_driver()
        wait = WebDriverWait(driver, 10)

        error_count = 0
        while error_count < AmazonScraper.ERROR_LIMIT:
            try:
                driver.get(AmazonScraper.URL)

                search_bar = wait.until(
                    ec.presence_of_element_located((By.ID, "twotabsearchtextbox")))
                
                search_bar.send_keys(search_query)
                search_bar.send_keys(Keys.RETURN)
                
                search_results = wait.until(
                    ec.presence_of_all_elements_located((By.CSS_SELECTOR, "div.s-result-item a.a-link-normal")))
                
                for result in search_results:
                    yield result.get_attribute("href")

                print(f'Finished getting search links on page {AmazonScraper.URL}')
                logging.info(f'Finished getting search links on page {AmazonScraper.URL}')
            except Exception as e:
                print(f'Error getting search links on page {AmazonScraper.URL}: {e}')
                logging.error(f'Error getting search links on page {AmazonScraper.URL}: {e}')
                error_count += 1
            finally:
                driver.quit()

    def get_product_info(self, link: str) -> dict:
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
            
            price_whole_text = price_whole.text.replace(',', '').replace('.', '')
            price_fraction_text = price_fraction.text
            price = float(price_whole_text + "." + price_fraction_text)
            currency = price_symbol.text
            product_info = {"price": price, "currency": currency}
    
            print(f'Finished getting product info on page {link}. Product info: {product_info}')
            logging.info(f'Finished getting product info on page {link}. Product info: {product_info}')
    
            return product_info
        except Exception as e:
            print(f'Error getting product info on page {link}: {e}')
            logging.error(f'Error getting product info on page {link}: {e}')
        finally:
            driver.quit()


    def get_product_infos(self, search_query: str) -> Generator:
        search_link_generator = self.get_search_links(search_query)
        search_link_generator = list(search_link_generator)[:10] # TODO: Delete after testing
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for link in search_link_generator:
                future = executor.submit(self.get_product_info, link)
                futures.append(future)

            for future in futures:
                result = future.result()
                if result:
                    yield result
