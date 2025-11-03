from dataclasses import dataclass


@dataclass
class AppConfig:
    name: str
    min_scrape_delay: int
    max_scrape_delay: int
