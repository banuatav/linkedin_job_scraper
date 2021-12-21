import collections
import uuid
from datetime import datetime

import os
import sys
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from . import data
from .scraper import PageScraper

# Data Class
JOB_FIELDS = ["id", "scraping_results", "source_code", "scraping_date", "job_name", "job_descr", "job_poster", "job_salary", "job_company", "email_id"]
JobAdData = collections.namedtuple("JobAdData", JOB_FIELDS)

def get_job_ads(scraper, email):
    job_ads = []
    for job in email.body_jobs:
        try:
            page = scraper.scrape_page(job["link"])
            extracted_data = data.extract_info(page["source_code"])

            job_data = JobAdData(id=str(uuid.uuid1()), scraping_date = str(datetime.utcnow()), **page, **extracted_data, email_id = email.id)
            job_ads.append(job_data)
        except:
            print("Skipping job.")
    
    return job_ads
