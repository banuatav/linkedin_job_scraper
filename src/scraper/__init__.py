import os
from selenium import webdriver
from linkedin_scraper import actions

from src.gmail import eml
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
