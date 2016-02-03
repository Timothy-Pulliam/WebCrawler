#!/usr/bin/env python

from pprint import pprint
import requests
import MySQLdb
from bs4 import BeautifulSoup

# Setup the database connection.
connection = MySQLdb.connect(user="root", passwd="root", host="localhost")
curs = connection.cursor()
curs.execute("CREATE DATABASE IF NOT EXISTS crawler;")
curs.execute("CREATE TABLE IF NOT EXISTS crawler.urls (\
url_id int NOT NULL,\
description VARCHAR(100),\
url varchar(200),\
PRIMARY KEY (url_id));")

# start pulling html
url = "http://www.reddit.com"
r = requests.get(url)
html = r.content
soup = BeautifulSoup(html, "html.parser")
links = soup.find_all('a')

data = {}
for link in links:
    data[link.text] = link.get("href")

for key in data:
    curs.execute("INSERT INTO TABLE crawler.urls VALUES (%s, %s);", (key, data[key])) 

curs.close()
connection.close()

# TESTING
print("done")