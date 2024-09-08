import json
from typing import Dict
import pytest
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEFAULT_DRIVER = "chrome"
DEFAULT_WAIT_TIMEOUT = 10
PROJECT_ROOT = Path.cwd().parent
SCREENSHOTS_PATH = str((PROJECT_ROOT / "screenshots/screenshot_{}.png").absolute())
CONFIG_PATH = str(PROJECT_ROOT/"config.json")

def init_config() -> Dict[str, any]:
    try:
        # read configs from json
        with open(CONFIG_PATH, 'r') as config_file:
            configs = json.loads(config_file.read())
            return configs
    except FileNotFoundError:
        # initialize default configs
        return {
            "drivers": [DEFAULT_DRIVER]
        }

config = init_config()
driver_params = config.get("drivers", [DEFAULT_DRIVER])

@pytest.fixture(params=driver_params, scope="class")
def driver_init(request):
    """Fixture to initialize WebDriver with options to disable notifications."""

    web_driver = None
    if request.param == "chrome":
        chrome_options = ChromeOptions()

        chrome_options.add_experimental_option(
            "prefs",
            {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.default_content_setting_values.notifications": 2
                # with 2 should disable notifications
            },
        )
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("start-maximized")

        # Initialize WebDriver
        web_driver = webdriver.Chrome(options=chrome_options)
        web_driver.maximize_window()
    elif request.param == "firefox":
        options = FirefoxOptions()
        options.set_preference('dom.webnotifications.enabled', False)

        web_driver = webdriver.Firefox(options=options)

    request.cls.driver = web_driver
    yield
    web_driver.quit()

def wait(driver, element):
    return WebDriverWait(driver, DEFAULT_WAIT_TIMEOUT).until(EC.element_to_be_clickable(element))

def pytest_exception_interact(node, report):
    if report.failed and hasattr(node.instance, "driver"):
        node.instance.driver.save_screenshot(SCREENSHOTS_PATH.format(report.when))

