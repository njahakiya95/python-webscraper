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
def weather_storer(weather_url):
    #url_connect is a Session object that allows you to persis
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

    return (weather_data_dict)
#Create a SQL database to store data from the dict
#Add code to save the data from the dict to a csv file
#Add code to plot seven day weather 
#Write main and prompt user for an input location 

URL = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=london+weather"
print(weather_storer(URL))