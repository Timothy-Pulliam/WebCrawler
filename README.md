# WebCrawler
A web crawler/scraper that when run through the terminal scrapes all links (HTML anchors) and saves them to a MySQL database. For example:

    ./crawler http://www.reddit.com reddit

Will scrape all links from www.reddit.com and place them inside a MySQL table named 'reddit' located 
inside a database named 'crawler_db'.

For installation, do the following.

    apt-get install mysql-server

    sudo /etc/init.d/mysql start

    git pull https://github.com/Timothy-Pulliam/WebCrawler

    pip3 install -r requirements.txt
