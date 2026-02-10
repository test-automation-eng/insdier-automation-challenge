import allure
from pages.home_page import HomePage
from pages.qa_jobs_page import QAJobsPage
from pages.qa_jobs_page import QAJobsPage
from pages.lever_page import LeverPage


@allure.title("Insider QA Jobs flow: filter and verify Lever redirect")
def test_home_page_flow(driver):
    home = HomePage(driver)
    qa_careers = QAJobsPage(driver)
    qa_jobs = QAJobsPage(driver)
    lever = LeverPage(driver)

    with allure.step("1) Open Insider homepage and verify main blocks loaded"):
        home.open_home()
        home.assert_home_loaded()

    with allure.step("2) Open QA careers page and click 'See all QA jobs'"):
        qa_careers.open_qa_jobs()
        qa_careers.click_see_all_qa_jobs()

    with allure.step("2b) Apply filters: Location=Istanbul, Turkey; Department=Quality Assurance"):
        qa_jobs.apply_filters()

    with allure.step("2c) Verify jobs list is present"):
        cards = qa_jobs.wait_jobs_present()

    with allure.step("3) Verify each job contains required Position/Department/Location values"):
        qa_jobs.assert_each_job_matches(cards)

    with allure.step("4) Click 'View Role' and confirm redirect to Lever application page"):
        qa_jobs.click_first_view_role(cards)
        lever.assert_is_lever()
