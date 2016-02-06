#!/usr/bin/env python

import requests
import MySQLdb
from bs4 import BeautifulSoup

# Setup the database connection.
url = "http://www.google.com"
table_name = "google"
create_database_sql = "CREATE DATABASE IF NOT EXISTS crawler CHARACTER SET utf8;"
create_table_sql = "CREATE TABLE IF NOT EXISTS crawler.%s (\
                    url_id int NOT NULL AUTO_INCREMENT,\
                    description VARCHAR(1000),\
                    url varchar(200),\
                    PRIMARY KEY (url_id));" %(table_name)

connection = MySQLdb.connect(user="root", passwd="root", host="localhost")
cursor = connection.cursor()
cursor.execute(create_database_sql)
cursor.execute(create_table_sql)

# start pulling html
r = requests.get(url)
html = r.content.decode("utf-8", errors="replace")
soup = BeautifulSoup(html, "html.parser")
links = soup.find_all('a')

data = {}
for link in links:
    data[link.text] = link.get("href")


for key in data:
    cursor.execute("INSERT INTO crawler.google (description, url) VALUES (%s, %s);", ( key.encode("utf-8"), data[key].encode("utf-8"))) 

# Auto commit is turned off by default
connection.commit()
cursor.close()
connection.close()
