#!/usr/bin/env python3  
# -*- coding: utf-8 -*- 
#===========================================================================
# Created By  : Nirmal Patel   
# Created Date: 1/2/2022
# version ='1.0'
#===========================================================================
"""
weather-scraper.py takes a user input location (if provided)
and outputs the current time, temperature, humidity, wind, and chance of precipitation. If no
input location is provided, the default location is the IP of the computer being used to run the code.

Furthermore, it also prints the 7 day forecast, along with the high/low temperature for each day. 

Google weather is used to perform the data scraping
"""

#Import libraries 
import requests
import argparse
from bs4 import BeautifulSoup as bs 
from requests.sessions import session

#USER_AGENT and LANGUAGE define the acceptable browsers and language used to return scraped data
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
LANGUAGE = "en-US,en;q=0.5"

def weather_fetcher(url):
    """Takes as an input, a user-input URL of Google Weather at a certain location and returns a dictionary with various weather data"""
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT          #User-Agent retrieves and presents Web content
    session.headers['Accept-Language'] = LANGUAGE       #Accept-Language defines the language intended for the end-user
    session.headers['Content-Language'] = LANGUAGE      #Content-Language defines the language to be used to pull the content
    weather_url = session.get(url)                      #Gets the user-entered URL of Google weather at a particular location 

    weather_data = bs(weather_url.text, "html.parser")  #create BeautifulSoup object and assign to weather_data

    weather_data_dict = {}  #weather_data_dict is a dict that holds the below extracted weather data from weather_data
    weather_data_dict['location'] = weather_data.find("div", attrs={"id": "wob_loc"}).text  
    weather_data_dict['time'] = weather_data.find("div", attrs={"id": "wob_dts"}).text
    weather_data_dict['current_temp'] = weather_data.find("span", attrs={"id": "wob_tm"}).text
    weather_data_dict['current_weather'] = weather_data.find("span", attrs={"id": "wob_dc"}).text
    weather_data_dict['precipitation'] = weather_data.find("span", attrs={"id": "wob_pp"}).text
    weather_data_dict['humidity'] = weather_data.find("span", attrs={"id": "wob_hm"}).text
    weather_data_dict['wind'] = weather_data.find("span", attrs={"id": "wob_ws"}).text

    seven_days_weather = [] #seven_day_weather is an array that holds the 7 days weather data from weather_data
    seven_days = weather_data.find("div", attrs={"id": "wob_dp"})
    
    for day in seven_days.findAll("div", attrs={"class": "wob_df"}):    #for each day in the seven_days array, find the html tag related to the weather data for each day
        day_name = day.findAll("div")[0].attrs['aria-label']  
        day_weather = day.find("img").attrs["alt"]              
        day_temp = day.findAll("span", {"class": "wob_t"})
        day_max = day_temp[0].text
        day_min = day_temp[2].text
        seven_days_weather.append({"name": day_name, "current_weather": day_weather, "max_temp": day_max, "min_temp": day_min})
    
    weather_data_dict['seven_days'] = seven_days_weather    #append seven_dats_weather to weather_data_dict 
    return weather_data_dict    #return

#Execute weatherscraper.py 
if __name__ == "__main__":
    URL = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"     #Google weather URL without location 
    url_parser = argparse.ArgumentParser(description="Extract weather data from user-input location")   #create and user argparse object called url_parser  
    url_parser.add_argument("location", nargs="?", help="""Location whose weather data will be extracted using Google Weather. Defaults to IP if no location provided""", default="")

    args = url_parser.parse_args()  #parse user-input arguement added after weatherscraper.py 
    location = args.location #assign user-input arguement to location
    URL += location #add location to the end of URL

    data = weather_fetcher(URL) #extract relevant weather data from weather_data_dict and print 
    print("Right now it is", data["time"], "in", data["location"])
    print("The weather is", data["current_temp"], "°F", "and", data["current_weather"])
    print("There is a ", data["precipitation"], "chance of precipitation")
    print("The humiditiy is", data["humidity"], "and the wind is", data["wind"])
    print("\n" * 3) #empty lines 
    print("The seven day forecast is:") #print seven days forecast

    for each_day in data["seven_days"]: #loop over each_day in seven_days and print the weather, max, and min temp for each_day 
        print("="*40, each_day["name"], "="*40)
        print("The weather forecast for", each_day["name"], "is", each_day["current_weather"])  
        print(f"The high is: {each_day['max_temp']}°F")
        print(f"The low is: {each_day['min_temp']}°F")