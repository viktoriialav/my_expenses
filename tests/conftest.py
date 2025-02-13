import allure_commons
import pytest
from appium import webdriver
from selene import browser, support

import config
from my_expenses_tests.utils import allure_browserstack


@pytest.fixture(scope='function', autouse=True)
def mobile_management():
    browser.config.driver = webdriver.Remote(command_executor=config.settings.remote_url,
                                             options=config.settings.driver_options)

    browser.config.timeout = config.settings.timeout

    browser.config._wait_decorator = support._logging.wait_with(context=allure_commons._allure.StepContext)

    yield

    session_id = browser.driver.session_id
    allure_browserstack.attach_screenshot(browser)
    allure_browserstack.attach_page_source(browser)

    browser.quit()

    if config.settings.is_bstack:
        allure_browserstack.attach_video(session_id, config.settings.user_name, config.settings.access_key)
