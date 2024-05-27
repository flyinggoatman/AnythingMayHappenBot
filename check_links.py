import mysql.connector
import requests
from decouple import config
import urllib3
import time

f = open("working.txt", "w")
f.write(f"{'Working links File.':#^100}\n")
f.close()
f = open("not_working.txt", "w")
f.write(f"{'Not Working Links File.':#^100}\n")
f.close()

# MySQL login information
SQL_HOST = config('SQL_HOST', default='localhost')
SQL_USER = config('SQL_USER')
SQL_PASS = config('SQL_PASS')
SQL_DATABASE = config('SQL_DATABASE')

# Create a connection to the database
cnx = mysql.connector.connect(
    host=SQL_HOST,
    user=SQL_USER,
    password=SQL_PASS,
    database=SQL_DATABASE
)

# Check the connection before fetching links
while True:
    try:
        cnx.ping(reconnect=True)
        break
    except mysql.connector.errors.OperationalError:
        time.sleep(5)

# Create a cursor object
cursor = cnx.cursor()

# Fetch all links from the database
query = "SELECT link FROM link"
cursor.execute(query)
results = cursor.fetchall()

total_links = len(results)  # Get the total number of links

print(f"{'Connected to database and beginning labeling.':#^100}")

# Check if each link is working or not
for index, result in enumerate(results, start=1):
    link = result[0]
    # Add 'http://' to the link
    url = 'http://' + link
    print(f"{index}/{total_links} checking {url}")
    try:
        cnx.ping(reconnect=True)
        # Send a GET request to the link
        response = requests.get(url, timeout=10)
        # Check the status code of the response
        if response.status_code == 200 or response.status_code == 301 or response.status_code == 302:
            print(f"{index}/{total_links} Link {url} is working.")
            with open("working.txt", mode="a") as f1:
                f1.write(f"{link}\n")
        else:
            print(f"{index}/{total_links} Link {url} is not working.")
            with open("not_working.txt", mode="a") as f2:
                f2.write(f"{link}\n")
    except (requests.exceptions.RequestException, urllib3.exceptions.LocationParseError):
        print(f"{index}/{total_links} Link {url} is not working.")
        with open("not_working.txt", mode="a") as f2:
            f2.write(f"{link}\n")

# Close the cursor and connection
cursor.close()
cnx.close()
print(f"{'The items have been labeled.':#^100}")
