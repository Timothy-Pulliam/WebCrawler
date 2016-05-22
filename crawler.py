#!/usr/bin/env python
"""A python script meant to be run from the command line. This script accepts the following arguments:
URL = a string object. where links will be scraped from
table_name = a string object. A MySQL table name where the links are stored.

The scraped links are stored in a MySQL database named 'crawler_db'. Because of this, MySQL/MariaDB is 
a required package."""

import requests
import MySQLdb
import _mysql_exceptions
from bs4 import BeautifulSoup
from sys import argv
from sys import exit

##################### VARIABLES #####################

help_message = '''Printing usage:

    ./crawler <url> <table_name>

For example:

    ./crawler http://www.reddit.com reddit

Will scrape all links from www.reddit.com and place them inside a MySQL table named 'reddit' located 
inside a database named 'crawler_db'.
'''
#################### EXECUTION ######################

if len(argv) != 3:
    print(help_message)
    exit()
else:
    pass
script, url, table_name = argv

# Try connecting to the already created 'crawler' DB. If this fails we must first create the crawler DB.
try:
    connection = MySQLdb.connect(user="root", passwd="root", host="localhost", db='crawler_db')
    cursor = connection.cursor()
except _mysql_exceptions.OperationalError as e:
    connection = MySQLdb.connect(user="root", passwd="root", host="localhost")
    cursor = connection.cursor()
    create_database_sql = "CREATE DATABASE IF NOT EXISTS crawler_db CHARACTER SET utf8;"
    cursor.execute(create_database_sql)
    cursor.execute('USE crawler_db;')
    
create_table_sql = "CREATE TABLE IF NOT EXISTS crawler_db.%s (\
                    url_id int NOT NULL AUTO_INCREMENT,\
                    description VARCHAR(1000),\
                    url varchar(200),\
                    PRIMARY KEY (url_id));" %(table_name)
cursor.execute(create_table_sql)

# start pulling html
request = requests.get(url)
html = request.content.decode("utf-8", errors="replace")
soup = BeautifulSoup(html, "html.parser")
links = soup.find_all('a')

# Finally, write the links and link descriptions to MySQL database. Make sure the data is encoded to UTF-8.
for link in links:
    cursor.execute("INSERT INTO "+ table_name +" (description, url) VALUES (%s, %s);", (link.text.encode("utf-8"), link.get('href').encode("utf-8"))) 

# Auto commit is turned off by default. This needs to be on for changes to be persistent.
connection.commit()
cursor.close()
connection.close()
