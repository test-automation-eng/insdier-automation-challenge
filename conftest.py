import os
import time
import pytest
import allure

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="Browser to run tests: chrome or firefox")
    parser.addoption("--headless", action="store_true", default=False,
                     help="Run browsers in headless mode")


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless")

    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        drv = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )

    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        drv = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
        drv.set_window_size(1920, 1080)

    else:
        raise ValueError("Unsupported browser. Use --browser=chrome or --browser=firefox")

    drv.implicitly_wait(0)
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Attach screenshot (and useful debug info) to Allure when a test fails."""
    outcome = yield
    rep = outcome.get_result()

    # Capture failures in test execution AND setup (fixture failures)
    if rep.failed and rep.when in ("setup", "call"):
        drv = item.funcargs.get("driver", None)
        if drv:
            ts = time.strftime("%Y%m%d-%H%M%S")

            # Screenshot
            allure.attach(
                drv.get_screenshot_as_png(),
                name=f"screenshot-{item.name}-{rep.when}-{ts}",
                attachment_type=allure.attachment_type.PNG
            )
            
            allure.attach(
                drv.current_url,
                name=f"current-url-{rep.when}",
                attachment_type=allure.attachment_type.TEXT
            )
