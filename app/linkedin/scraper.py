import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from linkedin_scraper import actions

_MORE_BUTTON_XPATH = "//footer/button[@aria-label='Click to see more description']"
_SELECTION_AREA = "grid"

class PageScraper:
    def __init__(self):
        self.driver = webdriver.Chrome(os.environ["CHROMEDRIVER"])
        actions.login(self.driver, os.environ["LINKEDIN_EMAIL"], os.environ["LINKEDIN_PW"])

    def _navigate_page(self, link):
        self.driver.get(link)
        time.sleep(2)

    def _click_see_more(self):
        try:
            # Click "See more" to load entire page
            _ = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, _MORE_BUTTON_XPATH))
            )
            see_more = self.driver.find_element_by_xpath(_MORE_BUTTON_XPATH
                                                         )
            see_more.click()
            time.sleep(2)
        except:
            print("Couldn't find see_more'")

    def _find_data(self):
        try:
            job_ad = self.driver.find_element_by_class_name(
                _SELECTION_AREA)
            scraping_results = job_ad.text
            source_code = job_ad.get_attribute('innerHTML')

            return scraping_results, source_code
        except:
            raise Exception("Couldn't find selection area")

    def scrape_page(self, link):
        # Navigate to page
        self._navigate_page(link)

        # Click 'See More': Expands on job information section
        self._click_see_more()

        # Find data
        scraping_results, source_code = self._find_data()

        return {"scraping_results":scraping_results, "source_code":source_code}
    def quit(self):
        self.driver.quit()
        
