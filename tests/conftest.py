from collections.abc import Generator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


@pytest.fixture
def driver(request) -> Generator[WebDriver, None, None]:
    # retrieves the current parameter value:
    browser = request.param.strip().lower() # .strip().lower() safeguard for accidental spaces and capitalization

    if browser == "chrome":
        active_driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install())
        )
    elif browser == "firefox":
        active_driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install())
        )
    else: # guard fails loudly if someone adds an unsupported browser
        raise ValueError(
            f"Unsupported browser: {browser!r}. Choose chrome or firefox." # !r small debugging aid, sets single quotes, making the value’s boundaries clear
        )

    active_driver.implicitly_wait(0) # Enforce explicit-waits-only strategy
    try:
        yield active_driver # returns a generator object that runs code piece by piece, pausing at each yield
    finally: # guarantees quit() runs even if the test raises an exception (safe-teardown pattern for fixtures managing external resources)
        active_driver.quit()

@pytest.fixture
def wait(driver: WebDriver):
    return WebDriverWait(driver, 10)


@pytest.fixture(scope="session")
def base_url() -> str:
    return "https://practicetestautomation.com"


def pytest_addoption(parser) -> None:
    parser.addoption(
        "--browsers",
        action="store",
        default="chrome,firefox",
        help="Comma-separated browser list, for example: --browsers=chrome,firefox",
    )


def pytest_generate_tests(metafunc) -> None:
    if "driver" in metafunc.fixturenames:
        browsers = [
            browser.strip().lower()
            for browser in metafunc.config.getoption("browsers").split(",")
            if browser.strip()
        ]
        if not browsers:
            raise pytest.UsageError("Pass at least one browser with --browsers.")

        metafunc.parametrize("driver", browsers, indirect=True)
