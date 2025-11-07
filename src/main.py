import logging

import hydra
from hydra.core.config_store import ConfigStore

from conf.config import AppConfig
from scraper_service import ScraperService
from scrapers.base_scraper import BaseScraper
from scrapers.realo_scraper import RealoScraper
from data_processing import DataProcessing
from scrapers.zimmo_scraper import ZimmoScraper

cs = ConfigStore.instance()
cs.store(name="base_config", node=AppConfig)

log = logging.getLogger(__name__)


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: AppConfig):
    log.info(f"Starting '{cfg.name}'!")

    # Add a new Scraper here everytime you implement one
    scrapers: list[BaseScraper] = [
        #RealoScraper(),
        ZimmoScraper(),
    ]

    scraper_service = ScraperService(scrapers=scrapers, user_agent=cfg.user_agent)
    scraped_data = scraper_service.scrape_websites()
    scraper_service.close_driver()

    if scraped_data:
        log.info(scraped_data)
        # Do something with the data
        # 1. Use the data processor to clean the data
        # 2. use the csv export to export to csv
        data_processing = DataProcessing(scraped_data)
        cleaned_data = data_processing.clean()
        # export the csv file - this is done within the processing script - does it need to come out?

        log.info("Do some")
    log.info(f"Stopping '{cfg.name}'!")


if __name__ == "__main__":
    main()
