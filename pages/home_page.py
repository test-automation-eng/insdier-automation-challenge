from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import os

class HomePage(BasePage):
    URL = os.getenv("BASE_URL")

    # Basic page is loaded checks:
    LOGO = (By.CSS_SELECTOR, "div[class='header-logo']")
    NAVBAR = (By.CSS_SELECTOR, "nav a[href='/partners']")
    FOOTER = (By.CSS_SELECTOR, "footer[id=footer]")

    def open_home(self):
        self.open(self.URL)

    def assert_home_loaded(self):
        self.wait_visible(self.NAVBAR)
        self.wait_visible(self.LOGO)
        self.wait_visible(self.FOOTER)
