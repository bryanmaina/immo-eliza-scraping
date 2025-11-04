from scrapers.base_scraper import BaseScraper
from selenium.webdriver.chrome.webdriver import WebDriver
from models import PropertyData
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging

log = logging.getLogger(__name__)


class ZimmoScrapper(BaseScraper):
    def __init__(self, website_url: str, municipalities: list[str], driver: WebDriver):
        super().__init__(website_url) #Calling BaseScraper.__init__
        self.driver = driver
        self.municipalities = municipalities
    
    def for_sale(self, municipalities): #Enter municipality and open search results page
        input_box = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Zoek een gemeente']")))
        input_box.clear()
        input_box.send_keys(municipalities)
        #Click "Zoeken" button (ENTER doesn't work)
        search_button = driver.find_element(By.CSS_SELECTOR, "#wrapper > div.content > div.hero-unit.home.home-nl.animated > div.container > zimmo-search-form > div.search > button")
        search_button.click()

    def collect_listing_urls(self): #For each listing grab the href of the listing (no click yet)
        #TO UPGRADE to collecting urls from all pages; so far - collecting the listing links of 1 page
        container = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.property-results")))
        listings = container.find_elements(By.CSS_SELECTOR, "div.property-item_photo-container > a")
        urls = [listing.get_attribute("href") for listing in listings]
        return urls
    
    def scrape_current_page(self): #By iteration, it opens each url in a tab
        urls = self.collect_listing_urls()
        all_data = []
        for url in urls:
            data = self.extract_data_from_url(url)
            all_data.append(data)
        return all_data


    def extract_data_from_url(self, url): #Collects data from a single listing page
        self.driver.get(url)
        property_id = self.driver.find_element(By.CSS_SELECTOR, "#main-features > div > div.title-row > p > font > font").text
        locality_name = self.driver.find_element(By.CSS_SELECTOR, "#main-features > div > div.title-row > div.section-title-block > h2 > span:nth-child(1) > font > font").text
        post_code = self.driver.find_element(By.CSS_SELECTOR, "#main-features > div > div.title-row > div.section-title-block > h2 > span:nth-child(1) > font > font").text
        price = self.driver.find_element(By.CSS_SELECTOR, "#tab-detail > div.container.main-container > div > div.pand-info-wrapper.main-features-wrapper.align-block-left > div > div > div:nth-child(1) > section > div > div.info-list > div:nth-child(1) > div.col-xsm-8.info-value > font > font").text
        property_type = self.driver.find_element(By.CSS_SELECTOR, "#main-features > div > div.row > div.col-sm-7.main-features-wrapper > ul > li:nth-child(3) > span > font > font").text
        type_of_sale = self.driver.find_element(By.CSS_SELECTOR, "").text
        number_of_rooms = self.driver.find_element(By.CSS_SELECTOR, "#main-features > div > div.row > div.col-sm-7.main-features-wrapper > ul > li:nth-child(5) > span > font > font").text
        living_area = self.driver.find_element(By.CSS_SELECTOR, "#main-features > div > div.row > div.col-sm-7.main-features-wrapper > ul > li:nth-child(4) > span > a > font > font").text
        garden_area = self.driver.find_element(By.CSS_SELECTOR, "#remainder > div.info-list > div > div.col-xs-5.info-value > i").text
        number_of_facade = self.driver.find_element(By.CSS_SELECTOR, "#construction > div.info-list > div:nth-child(1) > div.col-xs-5.info-value > font > font").text
        state_of_building = self.driver.find_element(By.CSS_SELECTOR, "#construction > div.info-list > div:nth-child(10) > div.col-xsm-5.info-value > font > font").text
        
        #Searching for properties key words in Layout list  
        try:
            layout_items = self.driver.find_elements(By.CSS_SELECTOR, "#tab-detail > div.container.main-container > div > div.pand-info-wrapper.main-features-wrapper.align-block-left > div > div > div:nth-child(2) > section > div")
            layout_texts = [item.text.strip().lower() for item in layout_items]

            terrace_area = "terras" in layout_texts or "terrace" in layout_texts  # handles both Dutch and English

        except Exception:
            layout_texts = []
            terrace_area = None

        #Searching for properties key words in main description 
        try:
            overview_text = self.driver.find_element(By.CSS_SELECTOR,"#description > div > p").text.lower()
            equipped_kitchen = "ingerichte keuken" in overview_text or "equipped kitchen" in overview_text
            furnished = "gemeubeld" in overview_text or "furnished" in overview_text
            open_fire = "haard" in overview_text or "fireplce" in overview_text
            swimming_pool = "zwembad" in overview_text or "swimming pool" in overview_text
        except Exception:
            overview_text = ""
            equipped_kitchen = furnished = open_fire = None

    return {
        "property_id": property_id,
        "locality_name": locality_name,
        "post_code": post_code, 
        "price": price,
        "property_type": property_type, 
        "type_of_sale": type_of_sale,
        "number_of_rooms": number_of_rooms,
        "living_area": living_area,
        "equiped_kitchen": equipped_kitchen,
        "furnished": furnished,
        "open_fire": open_fire,
        "terrace_area": terrace_area,
        "garden_area": garden_area,
        "number_of_facades": number_of_facades,
        "swimming_pool": swimming_pool,
        "state_of_building": state_of_building
    }
