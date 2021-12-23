import os
import sys

APP_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(APP_FOLDER)

from pymongo import MongoClient

from settings import DATABASE_NAME, HOST, PORT


if __name__ == '__main__':
    # Drop database
    print("\nDropping database", DATABASE_NAME)
    client = MongoClient(host=HOST, port=PORT) 
    client.drop_database(DATABASE_NAME)

    # Check if successful
    print ("\nDatabases remaining after drop:", client.list_database_names())

    # Close cient
    client.close()