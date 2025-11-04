import logging

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from models import PropertyData
from scrapers.base_scraper import BaseScraper

log = logging.getLogger(__name__)


class RealoScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://www.realo.be/")

    def scrape(self, driver: WebDriver) -> list[PropertyData]:
        """Scrapes property data from Realo."""
        driver.get(self.website_url)
        log.info(f"Scraping properties from {self.website_url}")

        log.info(f"page title: {driver.title}")
        properties: list[PropertyData] = []
        try:
            driver.implicitly_wait(2)
            h1_elements = driver.find_elements(By.CLASS_NAME, "type-search")
            for element in h1_elements:
                log.info(f"property_elements: {element.text}")
        except Exception as e:
            log.error(f"Could not find property elements on the page: {e}")

        log.info(f"Found {len(properties)} properties on {self.website_url}")
        return properties
