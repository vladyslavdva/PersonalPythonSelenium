from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from base_page import BasePage

class LoginPage(BasePage):

    LOGIN_PATH = "/practice-test-login/"
    SUCCESS_PATH = "/logged-in-successfully/"
    SUCCESS_MESSAGE = "Logged In Successfully"

    USERNAME = (By.ID, "username")
    PASSWORD = (By.NAME, "password")
    SUBMIT = (By.CLASS_NAME, "btn")
    PAGE_HEADING = (By.TAG_NAME, "h1")
    LOGOUT_LINK = (By.LINK_TEXT, "Log out")

    def __init__(self, driver: WebDriver, base_url: str, wait=None) -> None:
        super().__init__(driver, wait)
        self.base_url = base_url.rstrip("/") # safeguard for stripping

    @property
    def success_url(self) -> str:
        return f"{self.base_url}{self.SUCCESS_PATH}"

    @property
    def current_url(self) -> str:
        return self._driver.current_url

    def open(self) -> None:
        self._driver.get(f"{self.base_url}{self.LOGIN_PATH}")

    def login(self, username: str, password: str) -> None:
        self._wait.until(EC.visibility_of_element_located(self.USERNAME)).send_keys(username)
        self._wait.until(EC.visibility_of_element_located(self.PASSWORD)).send_keys(password)
        self._wait.until(EC.element_to_be_clickable(self.SUBMIT)).click()

    @property
    def success_message(self) -> str:
        heading = self._wait.until(EC.visibility_of_element_located(self.PAGE_HEADING))
        return heading.text

    @property
    def logout_link_is_visible(self) -> bool:
        link = self._wait.until(EC.visibility_of_element_located(self.LOGOUT_LINK))
        return link.is_displayed()
