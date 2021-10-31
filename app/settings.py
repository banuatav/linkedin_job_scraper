import os

# ENVIRONMENT
if not 'ENVIRONMENT' in os.environ:
    os.environ['ENVIRONMENT'] = 'DEBUG'
print("Starting app in {} mode".format(os.environ['ENVIRONMENT']))

# DATABASE
DATABASE_NAME = 'job_ads'