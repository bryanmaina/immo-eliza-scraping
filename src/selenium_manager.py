from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver


class SeleniumManager:
    def create_driver() -> WebDriver:
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.unhandled_prompt_behavior = "accept"
        options.timeouts = {"implicit": 5000}
        driver = webdriver.Chrome(options=options)
        return driver
