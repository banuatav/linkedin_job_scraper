import os

# ENVIRONMENT
if not "ENVIRONMENT" in os.environ:
    os.environ["ENVIRONMENT"] = "DEBUG"
if not "MAX_NUM_MAILS" in os.environ:
    os.environ["MAX_NUM_MAILS"] = "25"
print("Starting app in {} mode".format(os.environ["ENVIRONMENT"]))

# DATABASE
HOST = "localhost"
PORT = 27017
DATABASE_NAME = "job_ads"