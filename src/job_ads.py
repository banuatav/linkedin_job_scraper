import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

_MORE_BUTTON_XPATH = "//footer/button[@aria-label='Click to see more description']"
_SELECTION_AREA = "grid"


class JobAd():
    def __init__(self, link, driver=None, scrape=True, quit_driver=False):

        self.scraping_results = None
        self.driver = driver
        self.scrape = scrape
        self.quit_driver = quit_driver

        if self.driver == None:
            raise Exception("No driver is specified.")

        if self.scrape:
            self.scrape_page(link)

        if self.quit_driver:
            self.driver.quit()

    def scrape_page(self, link):

        # Get page
        self.driver.get(link)

        time.sleep(2)

        try:
            # Click "See more" to load entire page
            _ = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, _MORE_BUTTON_XPATH))
            )
            see_more = self.driver.find_element_by_xpath(_MORE_BUTTON_XPATH
                                                         )
            see_more.click()
        except:
            print("Couldn't find see_more'")

        time.sleep(2)

        # Find data
        try:
            # job_name = driver.find_element_by_xpath("//button[@class='jobs-save-button artdeco-button artdeco-button--3 artdeco-button--secondary']")
            # job_name = job_name.text
            self.job_ad = self.driver.find_element_by_class_name(
                _SELECTION_AREA)
            self.scraping_results = self.job_ad.text
            self.source_code = self.job_ad.get_attribute('innerHTML')
        except:
            print("Couldn't find selection area'")

        time.sleep(2)

    def __repr__(self):
        return "\n\n".join(self.scraping_results)
