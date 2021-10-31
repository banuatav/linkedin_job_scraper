import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from selenium import webdriver
from linkedin_scraper import actions

from gmail import eml
from .job_ads import JobAd


def scrape_jobs():
    job_details = eml.process.extract()
    driver = webdriver.Chrome(os.environ["CHROMEDRIVER"])
    actions.login(
        driver, os.environ["LINKEDIN_EMAIL"], os.environ["LINKEDIN_PW"])

    ads = []
    for i, link in enumerate([x["link"] for x in job_details]):
        print(i)
        ad_i = JobAd(driver=driver, link=link)
        ads.append(ad_i)
    driver.quit()
