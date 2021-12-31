#webscraper.py is used to scrape the content of various websites 
#and store the data in the MySQL database

import requests
from bs4 import BeautifulSoup as bs 

URL = "https://news.google.com/topstories?hl=en-US&gl=US&ceid=US:en"
r = requests.get(URL)

soup = bs(r.content, 'html5lib')
