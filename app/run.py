import scraper
from db import DATABASE

if __name__ == "__main__":
    ads = scraper.scrape_jobs()
