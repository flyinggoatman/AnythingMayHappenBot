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
print(f"{'Connected to database and begining labeling.':#^100}")
# Check if each link is working or not
for result in results:
    link = result[0]
    # Add 'http://' to the link
    url = 'http://' + link
    try:
        cnx.ping(reconnect=True)
        # Send a GET request to the link
        response = requests.get(url, timeout=10)
        print(f"checking {url}")
        # Check the status code of the response
        if response.status_code == 200 or response.status_code == 301 or response.status_code == 302:
            print(f"Link {url} is working.")
            f1 = open("working.txt", mode="a")
            
            f1.write(f"{link}\n")
            f1.close()
        else:    
            print(f"Link {url} is not working.")
            f = open("not_working.txt", mode="a")
            
            f.write(f"{link}\n")
            f.close()
    except requests.exceptions.RequestException or urllib3.exceptions.LocationParseError as e:
        print(f"Link {url} is not working.")
        f = open("not_working.txt", mode="a")
        
        f.write(f"{link}\n")
        f.close()
            

# Close the cursor and connection
cursor.close()
cnx.close()
print(f"{'The items have been labeled.':#^100}")




