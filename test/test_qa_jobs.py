import allure
from pages.qa_jobs_page import QAJobsPage

@allure.title("Insider QA Jobs flow: filter and verify Lever redirect")
def test_qa_page_flow(driver):
    qa_careers = QAJobsPage(driver)

    with allure.step("1) Open QA careers page and click 'See all QA jobs'"):
        qa_careers.open_qa_jobs()
        qa_careers.accept_cookies()
        qa_careers.click_see_all_qa_jobs()
        qa_careers.select_location("Istanbul, Turkiye")
        qa_careers.select_department("Quality Assurance")
        qa_careers.assert_each_job_matches(
        expected_position="Quality Assurance",
        expected_department="Quality Assurance",
        expected_location="Istanbul"
        )
        qa_careers.click_first_view_role()
        assert "lever.co" in driver.current_url, "Did not navigate to Lever application page"

   