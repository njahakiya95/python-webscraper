#!/usr/bin/env python3  
# -*- coding: utf-8 -*- 
#===========================================================================
# Created By  : Nirmal Patel   
# Created Date: 5/9/2022
# version ='2.0'
#===========================================================================
"""
weather-storer.py takes a user input location (if provided)
and outputs the current time, temperature, humidity, wind, and chance of precipitation. If no
input location is provided, the default location is the IP of the computer being used to run the code.

The user is given the option to output 1, 3 or 7 days weather

Google weather is used to perform the data scraping

Additionally the data is stored in a PostgreSQL database 
"""

#Import Libraries
import requests
import argparse
from requests import Session
from bs4 import BeautifulSoup as bs 

#USER_AGENT defines the acceptable browsers to scrape from and prevents our bot from being detected 
#LANGUAGE defines the language in which the scraping will be performed 
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
LANGUAGE = "en-US,en;q=0.5"

#Weather_storer function
def oneday_weather_storer(weather_url):
    #url_connect is a Session object that allows you to persist
    url_connect = requests.Session()
    url_connect.headers['User-Agent'] = USER_AGENT          #User-Agent retrieves and presents Web content
    url_connect.headers['Accept-Language'] = LANGUAGE       #Accept-Language defines the language intended for the end-user
    url_connect.headers['Content-Language'] = LANGUAGE      #Content-Language defines the language to be used to pull the content
    weather_url = url_connect.get(weather_url)              #Gets the user-entered URL of Google weather at a particular location 

    #weather_html stores html-parsed google weather page 
    weather_html = bs(weather_url.text, "html.parser")  

    #weather_data_dict{} stores weather data parsed from weather_html 
    weather_data_dict = {} 
    weather_data_dict['location'] = weather_html.find("div", attrs={"id": "wob_loc"}).text
    weather_data_dict['time'] = weather_html.find("div", attrs={"id": "wob_dts"}).text
    weather_data_dict['current_temp'] = weather_html.find("span", attrs={"id": "wob_tm"}).text
    weather_data_dict['current_weather'] = weather_html.find("span", attrs={"id": "wob_dc"}).text
    weather_data_dict['precipitation'] = weather_html.find("span", attrs={"id": "wob_pp"}).text
    weather_data_dict['humidity'] = weather_html.find("span", attrs={"id": "wob_hm"}).text
    weather_data_dict['wind'] = weather_html.find("span", attrs={"id": "wob_ws"}).text

    #Format and print data from weather_data_dict{} 
    print("\n" * 3)
    print("Right now it is", weather_data_dict["time"], "in", weather_data_dict["location"])
    print("The weather is", weather_data_dict["current_temp"], "°F", "and", weather_data_dict["current_weather"])
    print("There is a ", weather_data_dict["precipitation"], "chance of precipitation")
    print("The humiditiy is", weather_data_dict["humidity"], "and the wind is", weather_data_dict["wind"])
    print("\n" * 3)

    return "*******************************"

def sevenday_weather_storer(weather_url):
    #url_connect is a Session object that allows you to persist
    url_connect = requests.Session()
    url_connect.headers['User-Agent'] = USER_AGENT          #User-Agent retrieves and presents Web content
    url_connect.headers['Accept-Language'] = LANGUAGE       #Accept-Language defines the language intended for the end-user
    url_connect.headers['Content-Language'] = LANGUAGE      #Content-Language defines the language to be used to pull the content
    weather_url = url_connect.get(weather_url)              #Gets the user-entered URL of Google weather at a particular location 

    #weather_html stores html-parsed google weather page 
    weather_html = bs(weather_url.text, "html.parser")  
    
    #seven_days_weather is an array that stores the 7 days weather data 
    seven_days_weather = [] 
    seven_days = weather_html.find("div", attrs={"id": "wob_dp"})
    
    for day in seven_days.findAll("div", attrs={"class": "wob_df"}):    #for each day in the seven_days array, find the html tag related to the weather data for each day
        day_name = day.findAll("div")[0].attrs['aria-label']  
        day_weather = day.find("img").attrs["alt"]              
        day_temp = day.findAll("span", {"class": "wob_t"})
        day_max = day_temp[0].text
        day_min = day_temp[2].text
        seven_days_weather.append({"name": day_name, "current_weather": day_weather, "max_temp": day_max, "min_temp": day_min})

    for each_day in seven_days_weather["seven_days"]: #loop over each_day in seven_days and print the weather, max, and min temp for each_day 
        print("="*40, each_day["name"], "="*40)
        print("The weather forecast for", each_day["name"], "is", each_day["current_weather"])  
        print(f"The high is: {each_day['max_temp']}°F")
        print(f"The low is: {each_day['min_temp']}°F")

    return "*******************************"

if __name__ == "__main__":
    googlweather_url = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather+"   #googlweather_url stores google weather url
    location = input("Enter the name of the city whose weather you want to know: ")     #store user-input city name
    location_weather_url = googlweather_url+location    #location_weather_url concatenates location to googleweather_url

    print(oneday_weather_storer(location_weather_url))

    bool_seven_days = bool(input("Would you like to also view the 7 days weather? True or False: "))
    if bool_seven_days == True:
        print(sevenday_weather_storer(location_weather_url))
    else:
        print("Weather scraping complete!")