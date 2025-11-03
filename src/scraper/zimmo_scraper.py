from selenium.webdriver.chrome.webdriver import WebDriver


class ZimmoScrapper:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def open_page(self): 
        url = "https://www.zimmo.be/nl/"
        self.driver.get(url)
    
    def cookies(self):
        pass
    def for_sale(self): #random selecrtion of municipality 


    def click_links(self):

    def extract_data(self):
        try:
            price = driver.find_element(By.XPATH, ".//button[contains(@class,'accept')]")
        except:
            price = None
    





#Setting up the browser
#open main page
#go to for sale section
#collect or click on property links
#extract info from each property
#save data