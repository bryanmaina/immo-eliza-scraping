import json
import os
from abc import ABC, abstractmethod

from selenium.webdriver.remote.webdriver import WebDriver

from models import PropertyData

LAST_VISITED_SEARCH_FILE_NAME = "last_visited_search.txt"
LAST_VISITED_URL_FILE_NAME = "last_visited_url.txt"
ALL_PROPERTY_URLS_FILE_NAME = "all_property_urls.txt"


class BaseScraper(ABC):
    def __init__(
        self,
        name: str,
        website_url: str,
        cache_dir: str = "data",
    ) -> None:
        self.name = name
        self.website_url = website_url
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    @abstractmethod
    def scrape(self, driver: WebDriver) -> list[PropertyData]: ...

    def save_point(self, data: PropertyData, last_url: str):
        self.__save_inter_property(data)
        self.__save_last_visited_url(last_url)

    def __save_inter_property(self, data: PropertyData):
        cache_file = os.path.join(
            self.cache_dir,
            self.name,
            f"{data['property_id']}_property.json",
        )
        with open(cache_file, mode="wb", buffering=1) as f:
            json.dump(data, f)

    def __save_last_visited_url(self, last_url: str):
        urls_file = os.path.join(
            self.cache_dir,
            self.name,
            LAST_VISITED_URL_FILE_NAME,
        )
        with open(urls_file, mode="a+", buffering=1) as f:
            f.write(last_url)

    def get_last_visited_url(self) -> str:
        try:
            urls_file = os.path.join(
                self.cache_dir,
                self.name,
                ALL_PROPERTY_URLS_FILE_NAME,
            )
            with open(urls_file, mode="r") as f:
                lines = f.readline()
                if lines:
                    return lines[-1].strip()
                else:
                    return None  # Or raise an exception for an empty file
        except FileNotFoundError:
            return None

    def save_last_visited_search(self, last_url_info: dict) -> dict:
        urls_file = os.path.join(
            self.cache_dir,
            self.name,
            LAST_VISITED_SEARCH_FILE_NAME,
        )
        with open(urls_file, mode="w", buffering=1) as f:
            f.write(last_url_info, f)

    def get_last_visited_search(self) -> str:
        try:
            urls_file = os.path.join(
                self.cache_dir,
                self.name,
                LAST_VISITED_SEARCH_FILE_NAME,
            )
            with open(urls_file, mode="r") as f:
                lines = f.readline()
                if lines:
                    return lines[-1].strip()
                else:
                    return None  # Or raise an exception for an empty file
        except FileNotFoundError:
            return None
