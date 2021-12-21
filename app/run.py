from pymongo import MongoClient

import mail, linkedin, settings
from settings import DATABASE_NAME

if __name__ == "__main__":
    # # Connect to database
    # client = MongoClient() 
    # database = client[DATABASE_NAME]

    # Init 
    email_reader = mail.EmailReader()
    scraper = linkedin.PageScraper()

    # Retrieve emails and scrape jobs
    for id in email_reader.mail_ids:
        try:
            email = email_reader.read_email(id)
            job_ads = linkedin.get_job_ads(scraper, email)
            email_reader.archive_email(id)
        except Exception as e:
            print("Error: skipping email.", e)

    # Clean-up
    scraper.quit()
    email_reader.disconnect_server()
