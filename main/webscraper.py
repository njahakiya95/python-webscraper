#webscraper.py is used to scrape the content of various websites 
#and store the data in the MySQL database

import requests
import argparse
from bs4 import BeautifulSoup as bs 
from requests.sessions import session

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
# US english
LANGUAGE = "en-US,en;q=0.5"

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
        day_weather = day.find("img").attrs["alt"]
        day_temp = day.findAll("span", {"class": "wob_t"})
        day_max = day_temp[0].text
        day_min = day_temp[2].text
        seven_days_weather.append({"name": day_name, "current_weather": day_weather, "max_temp": day_max, "min_temp": day_min})
    
    weather_data_dict['seven_days'] = seven_days_weather
    return weather_data_dict

if __name__ == "__main__":
    URL = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"
    url_parser = argparse.ArgumentParser(description="Extract weather data from user-input location")
    url_parser.add_argument("location", nargs="?", help="""Location whose weather data will be extracted using Google Weather. Defaults to IP if no location provided""", default="")

    args = url_parser.parse_args()
    location = args.location 
    URL += location

    data = weather_fetcher(URL)
    print("Weather for:", data["location"])
    print("Now:", data["time"])
    print(f"Temperature now: {data['current_temp']}°F")
    print("Description:", data['current_weather'])
    print("Precipitation:", data["precipitation"])
    print("Humidity:", data["humidity"])
    print("Wind:", data["wind"])
    print("Next days:")
    for each_day in data["seven_days"]:
        print("="*40, each_day["name"], "="*40)
        print("Description:", each_day["current_weather"])
        print(f"Max temperature: {each_day['max_temp']}°F")
        print(f"Min temperature: {each_day['min_temp']}°F")