from scrapers.base_scraper import BaseScraper
from selenium.webdriver.chrome.webdriver import WebDriver
from models import PropertyData
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging
import re

log = logging.getLogger(__name__)


class ZimmoScrapper(BaseScraper):
    def __init__(self, municipalities: list[str]):
        super().__init__("https://www.zimmo.be/nl/") #Calling BaseScraper.__init__
        self.driver
        self.municipalities = municipalities 
        #municipalities = ["Antwerpen","Brugge","Brussel","Gent","Hasselt","Leuven","Aalst","Borgerhout","De Panne","Genk","Knokke-Heist","Mechelen","Oostende","Turnhout"]
    
    def for_sale(self, municipalities): #Enter municipality and open search results page
        input_box = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Zoek een gemeente']")))
        input_box.clear()
        input_box.send_keys(municipalities)
        search_button = self.driver.find_element(By.CSS_SELECTOR, "button.search_button")
        search_button.click()

    
    def collect_listing_urls(self): #For each listing, per each page, grab the href of the listing (no click yet)
        urls = []
        while True:
            container = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".property-results")))
            listings = container.find_elements(By.CSS_SELECTOR, ".property-item_title > a")
            page_urls = [listing.get_attribute("href") for listing in listings]
            urls.extend(page_urls)

            try:
                next_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.last a")))
                self.driver.execute_script("arguments[0].click();", next_button)
                WebDriverWait(self.driver, 5).until(EC.staleness_of(listings[0])) # Wait for page reload
            except Exception:
                break 
            
    def scrape_current_page(self): #By iteration, each url opens in a tab
        urls = self.collect_listing_urls()
        all_data = []
        for url in urls:
            data = self.extract_data_from_url(url)
            all_data.append(data)
        return all_data

    #Collects data from a single listing page
    def extract_data_from_url(self, url):
        self.driver.get(url)
        property_id = self.driver.find_element(By.CSS_SELECTOR, ".title-row p").text
        price = self.driver.find_element(By.CSS_SELECTOR, "div.price-box > div > span").text
        type_of_sale = self.driver.find_element(By.CSS_SELECTOR, " ").text
        #property_type = self.driver.find_element(By.CSS_SELECTOR, "ul.main-features li:nth-child(3) .feature-value").text
        #number_of_rooms = self.driver.find_element(By.CSS_SELECTOR, "ul.main-features li:nth-child(5) .feature-value").text
        #living_area = self.driver.find_element(By.CSS_SELECTOR, "ul.main-features li:nth-child(4) .feature-value").text
        #garden_area = self.driver.find_element(By.CSS_SELECTOR, "#remainder > div.info-list > div > div.col-xs-5.info-value > i").text
        
        # Split locality and postcode via regex
        full_address = self.driver.find_element(By.CSS_SELECTOR, "#main-features .section-title-block h2 span:first-child").text
        match = re.search(r'(\d{4})\s+([A-Za-zÀ-ÿ\-]+)', full_address)
        if match:
            post_code = match.group(1)
            locality_name = match.group(2)
        
        #Searching for condition of building, type,living area, rooms, 
        #checking the number of facades in Main features at the beginning of page
        main_features = self.driver.find_elements(By.CSS_SELECTOR, ".main-features li")
        data = {}
        for li in main_features:
            try:
                label = li.find_element(By.CSS_SELECTOR, ".feature-label").text.strip().lower()
                value = li.find_element(By.CSS_SELECTOR, ".feature-value").text.strip().lower()
                data[label] = value #Creating a dictionary with parameters from this block
            except:
                continue 
            
        state_of_building = data.get("Conditie", None)
        property_type = data.get("Type", None)
        living_area = data.get("Living area", None)
        number_of_rooms = data.get("Slaapkamers", None)
        
        number_of_facade = data.get("bebouwing", None)

        if number_of_facade == "gesloten":
            number_of_facade = 1
        elif number_of_facade == "open":
            number_of_facade = 4
        elif number_of_facade == "halfopen":
            number_of_facade = 2


        #Searching for key word ("terrace") in Layout block  
        try:
            layout_items = self.driver.find_elements(By.CSS_SELECTOR, "#tab-detail .section-title-block")
            layout_texts = [item.text.strip().lower() for item in layout_items]
            terrace_area = "terras" in layout_texts or "terrace" in layout_texts  #Handles both Dutch and English

        except Exception:
            layout_texts = []
            terrace_area = None

        #Searching for other key words in Main description 
        try:
            overview_text = self.driver.find_element(By.CSS_SELECTOR,"#description > div > p").text.lower()
            equipped_kitchen = "ingerichte keuken" in overview_text or "equipped kitchen" in overview_text
            furnished = "gemeubeld" in overview_text or "furnished" in overview_text
            open_fire = "haard" in overview_text or "fireplce" in overview_text
            swimming_pool = "zwembad" in overview_text or "swimming pool" in overview_text
            garden_area = "tuin" in overview_text or "garden" in overview_text
            
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
            "number_of_facades": number_of_facade,
            "swimming_pool": swimming_pool,
            "state_of_building": state_of_building
        }
