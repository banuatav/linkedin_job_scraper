# LinkedIn Job Page Scraper

Scrapes LinkedIn job pages from job alerts.

- LinkedIn alerts are set up for relevant job titles / regions /  etc.
- Alerts are received in a gmail mailbox.
- App read alerts from mailbox (and archives processed emails).
- App extracts urls for job pages from alerts.
- App scrapes job pages (using Selenium) and extracts info (job description, salary, etc).
- Finally all data is inserted in a MongoDB database.

Builds on scraping tools provided by https://github.com/joeyism/linkedin_scraper.


# Requirements
- LinkedIn account
  - email (gmail account, see below) and password stored at environment variables `LINKEDIN_EMAIL` and `LINKEDIN_PW` (TODO: same env var gmail and li email)
  - email alerts for job titles of interest
- Gmail account
  - IMAP access enabled (see <a href="https://support.google.com/mail/answer/7126229?hl=en#zippy=%2Cstep-check-that-imap-is-turned-on">here</a>)
  - App password created (see <a href="https://support.google.com/mail/answer/185833?hl=en-GB">here</a>)
  - email and app password stored at environment variables `LIS_GMAIL` and `LIS_APP_PW`
  - email filter so that alerts are automatically labeled with "new-job-alerts" (TODO: change to env var)
- Selenium chrome driver
  -  can be downloaded from https://chromedriver.chromium.org/downloads
  -  location stored at environment variable `CHROMEDRIVER` (TODO: allow other browsertypes)
- A MongoDB installation (see <a href="https://docs.mongodb.com/manual/installation/">here</a>)
- Packages from `requirement.txt` installed in python environment.

# Usage
Run command `python app/run.py` to start the process.

The default number of mais to read is 25, but can be changed with environment variable `MAX_NUM_MAILS`.
