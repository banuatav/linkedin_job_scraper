from pymongo import MongoClient

client = MongoClient()
DATABASE = client['job_ads']