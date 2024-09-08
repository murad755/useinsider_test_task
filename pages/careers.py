import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

class CareersPage:
    def __init__(self, driver):
        self.driver = driver

    see_all_teams_button = (By.CSS_SELECTOR,
                            ".btn.btn-outline-secondary.rounded.text-medium.mt-5.mx-auto.py-3.loadmore")
    quality_assurance_button = (By.XPATH,
                                "//h3[@class='text-center mb-4 mb-xl-5'][contains(text(), 'Quality Assurance')]")
    see_all_qa_jobs_button = (By.XPATH,
                              "//a[contains(text(), 'See all QA jobs')]")
    filter_location = (By.XPATH,
                       '//span[contains(@class, "select2-selection--single")]')
    istanbul_option = (By.XPATH,
                       '//li[contains(@class, "select2-results__option") and text()="Istanbul, Turkey"]')
    filter_department = (By.XPATH,
                         '//span[contains(@class, "select2-selection--single") and @aria-labelledby="select2-filter-by-department-container"]')
    qa_department = (By.XPATH,
                     '//li[contains(@class, "select2-results__option") and text()="Quality Assurance"]')
    job_positions = (By.XPATH,
                     "//div[contains(@class, 'position-list-item')]")
    apply_now_button = (By.XPATH,
                        ".//a[contains(text(), 'View Role')]")

    def click_see_all_teams(self):
        wait = WebDriverWait(self.driver, 10)  # Adjust the waiting time as needed
        see_all_teams_element = wait.until(EC.visibility_of_element_located(self.see_all_teams_button))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", see_all_teams_element)
        self.driver.execute_script("arguments[0].click();", see_all_teams_element)

    def click_quality_assurance(self):
        wait = WebDriverWait(self.driver, 10)  # Adjust the waiting time as needed
        see_all_teams_element = wait.until(EC.visibility_of_element_located(self.quality_assurance_button))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", see_all_teams_element)
        self.driver.execute_script("arguments[0].click();", see_all_teams_element)

    def click_see_all_qa_jobs(self):
        self.driver.find_element(*self.see_all_qa_jobs_button).click()
        time.sleep(4)

    def filter_jobs(self):
        wait = WebDriverWait(self.driver, 10)
        filter_location_element = wait.until(EC.visibility_of_element_located(self.filter_location))
        filter_location_element.click()

        wait = WebDriverWait(self.driver, 10)
        istanbul_option_element = wait.until(EC.visibility_of_element_located(self.istanbul_option))
        istanbul_option_element.click()

        time.sleep(2)

        wait.until(EC.visibility_of_element_located(self.filter_department)).click()

        wait.until(EC.visibility_of_element_located(self.qa_department)).click()

    def get_job_positions(self):
        element = self.driver.find_element(*self.job_positions)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.visibility_of_all_elements_located(self.job_positions))

    def click_apply_now(self, job_element):
        apply_button = job_element.find_element(*self.apply_now_button)
        apply_button.click()