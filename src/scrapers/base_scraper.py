from abc import ABC, abstractmethod

from selenium.webdriver.chrome.webdriver import WebDriver

from models import PropertyData


class BaseScraper(ABC):
    def __init__(self, website_url: str) -> None:
        self.website_url = website_url

    @abstractmethod
    def scrape(self, driver: WebDriver) -> list[PropertyData]: ...
