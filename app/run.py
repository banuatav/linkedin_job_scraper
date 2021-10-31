from pymongo import MongoClient

import scraper
from settings import DATABASE_NAME

if __name__ == "__main__":
    # Connect to database
    client = MongoClient() 
    database = client[DATABASE_NAME]

    # Scrape adds
    ads = scraper.scrape_jobs()
