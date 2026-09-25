from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from settings import WAIT_TIMEOUT_SECONDS

class BasePage:
    def __init__(self, driver, wait=None):
        self._driver = driver
        self._wait = (
            wait if wait is not None
            else WebDriverWait(driver, WAIT_TIMEOUT_SECONDS)
        )