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

    seven_days_weather = []
    seven_days = weather_data.find("div", attrs={"id": "wob_dp"})
    
    for day in seven_days.findAll("div", attrs={"class": "wob_df"}):
        day_name = day.findAll("div")[0].attrs['aria-label']
        day_weather = day.findAll("img").attrs["alt"]
        day_temp = day.findAll("span", {"class": "wob_t"})
        day_max = day_temp[0].text
        day_min = day_temp[2].text
        seven_days_weather.append({"name": day_name, "current_weather": day_weather, "max_temp": day_max, "min_temp": day_min})
    
    weather_data_dict['seven_days'] = seven_days_weather
    return weather_data_dict