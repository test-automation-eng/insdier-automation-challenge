import allure
from pages.home_page import HomePage

@allure.title("Insider QA Jobs flow: filter and verify Lever redirect")
def test_home_page_flow(driver):
    home = HomePage(driver)


    with allure.step("1) Open Insider homepage and verify main blocks loaded"):
        home.open_home()
        home.assert_home_loaded()
