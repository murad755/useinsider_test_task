from tests.conftest import wait
from selenium.webdriver.common.by import By

class InsiderHomePage:
    def __init__(self, driver):
        self.driver = driver

    company_button = (By.CSS_SELECTOR, 'li.nav-item:nth-child(6) > a:nth-child(1)')
    careers_button = (By.CSS_SELECTOR, 'a[class="dropdown-sub"][href*="careers"]')

    def click_company(self):
        more_element = wait(self.driver, self.company_button)
        more_element.click()

    def click_careers(self):
        careers_element = wait(self.driver, self.careers_button)
        careers_element.click()
