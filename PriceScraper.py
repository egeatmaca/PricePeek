from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager


class PriceScraper:
    def __init__(self, search_query):
        self.url = "https://www.amazon.com/"
        self.search_query = search_query
        self.driver = self.get_driver()

    def get_options(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}

        return chrome_options

    def get_driver(self):
        driver = webdriver.Chrome(options=self.get_options())

        return driver
    
    def get_search_links(self):
        self.driver.get(self.url)
        search_bar = self.driver.find_element(By.ID, "twotabsearchtextbox")
        search_bar.send_keys(self.search_query)
        search_bar.send_keys(Keys.RETURN)

        try:
            search_results = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(By.CSS_SELECTOR, "div.s-result-item")
            )
            search_links = [result.find_element(By.CSS_SELECTOR, "a.a-link-normal").get_attribute("href") for result in search_results]
            return search_links
        except:
            self.driver.quit()

    def get_prices(self, links):
        for link in links:
            self.driver.get(link)
            try:
                price = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(By.ID, "priceblock_ourprice")
                )
                yield price.text
            except Exception as e:
                print(e)

    def quit(self):
        self.driver.quit()

if __name__ == "__main__":
    scraper = PriceScraper("laptop")
    links = scraper.get_search_links()
    print(links)
    print(scraper.get_prices(links))
    scraper.quit()
