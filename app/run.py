import os
from datetime import datetime

from pymongo import MongoClient

import mail, linkedin, settings
from settings import DATABASE_NAME, HOST, PORT

if __name__ == "__main__":
    # Connect to database. If the database doesn’t exist, then MongoDB 
    # creates it for you when you perform the first operation on the database.

    client = MongoClient(host=HOST, port=PORT) 
    database = client[DATABASE_NAME]
    col_emails = database.emails
    col_job_ads = database.col_job_ads

    # Init 
    email_reader = mail.EmailReader(max_nr_mails=int(os.environ["MAX_NUM_MAILS"]))
    scraper = linkedin.PageScraper()

    print("Start scraping: {}".format(str(datetime.now())))
    for i, id in enumerate(email_reader.mail_ids):
        if i % 10 ==0:
            print("-- Email {} / {}".format(i, len(email_reader.mail_ids)))
        try:
            # Retrieve emails and scrape jobs
            email = email_reader.read_email(id)
            job_ads = linkedin.get_job_ads(scraper, email)

            # Insert data in database
            result_email = col_emails.insert_one(email._asdict())
            if job_ads: # Need to be nonempty
                result_job_ads = col_job_ads.insert_many([x._asdict() for x in job_ads])

            # Archive email 
            email_reader.archive_email(id)            
        except Exception as e:
            print("---- Error: skipping email {}".format(i))
            if 'result_email' in locals():
                print("Failed mail:", result_email)
            if 'result_job_ads' in locals():
                print("Failed job_ads:", result_job_ads)
            print(e)
            
    # Clean-up
    print("Finished scraping: {}".format(str(datetime.now())))
    scraper.quit()
    email_reader.disconnect_server()
    client.close()