import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from error_handling import retry
from models import PropertyData
from scrapers.base_scraper import BaseScraper

log = logging.getLogger(__name__)


class ScraperService:
    def __init__(self, scrapers: list[BaseScraper], user_agent: str):
        self.scrapers = scrapers
        self.user_agent = user_agent
        self.driver = self._init_driver()

    def _init_driver(self) -> WebDriver:
        """Initializes the Chrome web driver."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"--user-agent={self.user_agent}")
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    @retry(retries=3, delay=5)
    def scrape_website(self, scraper: BaseScraper) -> list[PropertyData]:
        """Scrapes a single website using the given scraper."""
        log.info(f"Scraping {scraper.website_url}...")
        return scraper.scrape(self.driver)

    def scrape_websites(self) -> list[PropertyData]:
        """Scrapes all websites from the list of scrapers."""
        all_data = []
        for scraper in self.scrapers:
            try:
                data = self.scrape_website(scraper)
                all_data.extend(data)
                log.info(f"Successfully scraped {scraper.website_url}.")
            except Exception as e:
                log.error(f"Failed to scrape {scraper.website_url}: {e}")
        return all_data

    def close_driver(self):
        """Closes the web driver."""
        self.driver.quit()
