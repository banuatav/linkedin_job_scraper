import mysql.connector as mysql

db = mysql.connect(host="localhost", user="root")
cursor = db.cursor()

DATABASE_NAME = "job_ads"

# Create database
cursor.execute("DROP DATABASE  IF EXISTS {};".format(DATABASE_NAME))
cursor.execute("CREATE DATABASE {};".format(DATABASE_NAME))
print("Database {} created".format(DATABASE_NAME))

# Print results
cursor.execute("SHOW DATABASES;")
databases = cursor.fetchall()
print("-- List of all databases:")
for database in databases:
    print("---- " + str(database[0]))

db.commit()
cursor.close()
db.close()

# Connect to db
db = mysql.connect(host="localhost", user="root", database=DATABASE_NAME)
cursor = db.cursor()

# Create tables
cursor.execute(
    "CREATE TABLE ads (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, creation_time DATETIME, job_name VARCHAR(100), job_descr MEDIUMTEXT, job_poster MEDIUMTEXT, salary MEDIUMTEXT, company MEDIUMTEXT)"
)

# Print results
cursor.execute("SHOW TABLES")
print("-- List of all tables:")
tables = cursor.fetchall()
for table in tables:
    print("---- " + str(table[0]))


db.commit()
cursor.close()
db.close()
