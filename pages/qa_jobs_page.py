import os
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from pages.base_page import BasePage

class QAJobsPage(BasePage):
    URL = os.getenv("QA_JOBS_URL")

    # Locators for QA jobs page:
    SEE_ALL_QA_JOBS = (By.XPATH, "//a[contains(text(),'See all QA jobs')]")
    COOKIE_ACCEPT = (By.XPATH, "//a[contains(text(),'Accept All')]")
    FILTER_BY_LOCATION = (By.ID, "filter-by-location")
    FILTER_BY_DEPARTMENTS = (By.ID, "filter-by-department")
    JOB_LIST = (By.ID, "jobs-list")
    JOB_CARDS = (By.CSS_SELECTOR, "#jobs-list > div")
    VIEW_ROLE = (By.XPATH, "//a[contains(text(),'View Role')]")
    
    def open_qa_jobs(self):
        self.open(self.URL)

    def accept_cookies(self):
        self.click_if_present(self.COOKIE_ACCEPT)    

    def click_see_all_qa_jobs(self):
        self.click(self.SEE_ALL_QA_JOBS) 
        
    def select_location(self, location_text: str):
        self.wait.until(
             EC.presence_of_element_located(
               (By.XPATH, f"//select[@id='filter-by-location']/option[normalize-space()='{location_text}']")
            )
        )
        el = self.wait_clickable(self.FILTER_BY_LOCATION)
        Select(el).select_by_visible_text(location_text)
        
    def select_department(self, department_text: str):
        self.wait.until(
             EC.presence_of_element_located(
               (By.XPATH, f"//select[@id='filter-by-department']/option[normalize-space()='{department_text}']")
            )
        )
        el = self.wait_clickable(self.FILTER_BY_DEPARTMENTS)
        Select(el).select_by_visible_text(department_text)   

    def get_job_cards(self):
        time.sleep(2.5)
        self.wait_clickable(self.JOB_LIST)
        cards = self.wait_all_visible(self.JOB_CARDS)
        cards = [c for c in cards if c.is_displayed()]
        return cards

    def assert_each_job_matches(self,
                                expected_position="Quality Assurance",
                                expected_department="Quality Assurance",
                                expected_location="Istanbul"):
        cards = self.get_job_cards()
        assert len(cards) > 0, "No job cards found"

        for index, card in enumerate(cards, start=1):
            card_text = card.text.strip()

            with allure.step(f"Validate job card #{index}"):
                assert expected_position.lower() in card_text.lower(), \
                    f"[Card {index}] Position does not contain '{expected_position}'"

                assert expected_department.lower() in card_text.lower(), \
                    f"[Card {index}] Department does not contain '{expected_department}'"

                assert expected_location.lower() in card_text.lower(), \
                    f"[Card {index}] Location does not contain '{expected_location}'"    

    def click_first_view_role(self):
        main_window = self.driver.current_window_handle
        existing_windows = set(self.driver.window_handles)

        view_role = self.wait_clickable(self.VIEW_ROLE)
        self.scroll_into_view(view_role)
        view_role.click()

        # Wait for either: URL changed in same tab OR a new window opened
        self.wait.until(lambda d: "lever.co" in d.current_url or len(d.window_handles) > len(existing_windows))

        # If new tab opened, switch to it
        new_windows = set(self.driver.window_handles) - existing_windows
        if new_windows:
            self.driver.switch_to.window(new_windows.pop())

            # Firefox often starts new tabs as about:blank; wait until it navigates
            self.wait.until(lambda d: "lever.co" in d.current_url and d.current_url != "about:blank")

        else:
            # Same tab case: ensure it actually navigated
            self.wait.until(lambda d: "lever.co" in d.current_url)

