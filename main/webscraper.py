#webscraper.py is used to scrape the content of various websites 
#and store the data in the MySQL database

import requests
from bs4 import BeautifulSoup as bs 
from requests.sessions import session

def weather_fetcher(url):
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    weather_url = session.get(url)

    weather_data = bs(weather_url.text, "html.parser")

    weather_data_dict = {}
    weather_data_dict['location'] = weather_data.find("div", attrs={"id": "wob_loc"}).text
    weather_data_dict['time'] = weather_data.find("div", attrs={"id": "wob_dts"}).text
    weather_data_dict['current_temp'] = weather_data.find("span", attrs={"id": "wob_tm"}).text
    weather_data_dict['current_weather'] = weather_data.find("span", attrs={"id": "wob_dc"}).text
    weather_data_dict['precipitation'] = weather_data.find("span", attrs={"id": "wob_pp"}).text
    weather_data_dict['humidity'] = weather_data.find("span", attrs={"id": "wob_hm"}).text
    weather_data_dict['wind'] = weather_data.find("span", attrs={"id": "wob_ws"}).text