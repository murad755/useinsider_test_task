import time

import pytest

from pages.homePage import InsiderHomePage
from pages.careers import CareersPage

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


def close_cookie_banner(driver):
    try:
        cookie_accept_button_xpath = '//a[contains(@class, "cli_action_button")]'
        wait = WebDriverWait(driver, 10)
        cookie_accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, cookie_accept_button_xpath)))
        cookie_accept_button.click()
    except TimeoutException:
        print("Cookie banner not found or accept button not clickable")

@pytest.mark.usefixtures("driver_init")
class TestInsider:
    def test_insider_careers(self):
        self.driver.get("https://useinsider.com/")

        close_cookie_banner(self.driver)
        home_page = InsiderHomePage(self.driver)
        home_page.click_company()
        home_page.click_careers()

        careers_page = CareersPage(self.driver)
        careers_page.click_see_all_teams()
        careers_page.click_quality_assurance()
        careers_page.click_see_all_qa_jobs()
        careers_page.filter_jobs()

        job_positions = careers_page.get_job_positions()

        job = None
        for job in job_positions:
            # Simulate hovering the cursor over the work position
            hover = ActionChains(self.driver).move_to_element(job)
            hover.perform()

            print("Testing job:", job.text)

            assert "Quality Assurance" in job.text
            assert "Istanbul, Turkey" in job.text
            assert "View Role" in job.text
            break

        current_window = self.driver.current_window_handle

        time.sleep(2)

        careers_page.click_apply_now(job)

        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.number_of_windows_to_be(2))

        for window_handle in self.driver.window_handles:
            if window_handle != current_window:
                self.driver.switch_to.window(window_handle)
                current_url = self.driver.current_url
                print(current_url)
                assert "lever" in current_url, f"Expected 'lever' in the URL, but got {current_url}"
                break