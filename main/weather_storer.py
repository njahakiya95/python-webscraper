#!/usr/bin/env python3  
# -*- coding: utf-8 -*- 
#===========================================================================
# Created By  : Nirmal Patel   
# Created Date: 5/9/2022
# version ='2.0'
#===========================================================================

"""
weather-storer.py takes a user input location (if provided)
and outputs the current time, temperature, humidity, wind, and chance of precipitation. Furthermore, 
the seven day weather forecast (forecast, high, and low) is printed based on a user_input boolean variable. 

oneday_weather_storer() handles the one day weather
sevenday_weather_stored() handles the seven day weather

In addition to printing the weather information, it is automativally saved in a
PostgreSQL datbase and the user is given the option to save it in a CSV file. 
"""

#Import Libraries
import requests
from requests import Session
from bs4 import BeautifulSoup as bs
import csv 
import psycopg2
import os 

#USER_AGENT defines the acceptable browsers to scrape from and prevents our bot from being detected 
#LANGUAGE defines the language in which the scraping will be performed 
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
LANGUAGE = "en-US,en;q=2.0"

#oneday_weather_storer 
def oneday_weather_storer(weather_url):
    #url_connect is a Session object that allows you to create a persistent connection 
    url_connect = requests.Session()
    url_connect.headers['User-Agent'] = USER_AGENT          #User-Agent retrieves and presents Web content
    url_connect.headers['Accept-Language'] = LANGUAGE       #Accept-Language defines the language intended for the end-user
    url_connect.headers['Content-Language'] = LANGUAGE      #Content-Language defines the language to be used to pull the content
    weather_url = url_connect.get(weather_url)              #Downloads html of weather data at user-entered location 

    #weather_html stores html-parsed google weather page in BeautifulSoup object
    weather_html = bs(weather_url.text, "html.parser")  

    #weather_data_dict{} stores weather data parsed from weather_html 
    weather_data_dict = {} 
    weather_data_dict['location'] = weather_html.find("div", attrs={"id": "wob_loc"}).text.split(",")[0]
    weather_data_dict['time'] = weather_html.find("div", attrs={"id": "wob_dts"}).text
    weather_data_dict['current_temperature'] = weather_html.find("span", attrs={"id": "wob_tm"}).text
    weather_data_dict['current_weather'] = weather_html.find("span", attrs={"id": "wob_dc"}).text
    weather_data_dict['precipitation'] = weather_html.find("span", attrs={"id": "wob_pp"}).text
    weather_data_dict['humidity'] = weather_html.find("span", attrs={"id": "wob_hm"}).text
    weather_data_dict['wind'] = weather_html.find("span", attrs={"id": "wob_ws"}).text

    #Format and print data from weather_data_dict{} 
    print("\n" * 1)
    print("Right now it is", weather_data_dict["time"], "in", weather_data_dict["location"])
    print("The weather is", weather_data_dict["current_temperature"], "°F", "and", weather_data_dict["current_weather"])
    print("There is a", weather_data_dict["precipitation"], "chance of precipitation")
    print("The humiditiy is", weather_data_dict["humidity"], "and the wind is", weather_data_dict["wind"])
    print("\n" * 1)

    #csv_title variable holds the title of the csv file using the location html id
    #.split(,)[0] removes the State and Zipcode from the html tag
    #.replaces whitespaces for city names that are more than one word long 
    csv_title = weather_html.find("div", attrs={"id": "wob_loc"}).text.split(',')[0].replace(" ", "")

    #Create a directory to store one-day data csv files 
    try:
        os.mkdir("./OneDayData")
    except OSError as e:
        pass

    #Save and output a csv file with the one-day weather data 
    csv_file = f"{csv_title}_oneday_data.csv"
    file = open("./OneDayData/" + csv_file, "w")
    file_writer = csv.DictWriter(file, weather_data_dict.keys())
    file_writer.writeheader()
    file_writer.writerow(weather_data_dict)
    file.close()

    #Connect to weather database that contains the oneday table 
    conn = psycopg2.connect(database="weather", user="nirmal", password="password", host="127.0.0.1", port="5432")
    
    #create cursor object to interact with the weather database 
    curs = conn.cursor()

    #Open <location>_oneday_data.csv, read from the file and save data to database
    with open("./OneDayData/" + csv_file, 'r') as f:
        next(f)
        curs.copy_from(f, 'oneday_data', sep=',')
    
    conn.commit()

    return ("\n")

#sevenday_weather_storer
def sevenday_weather_storer(weather_url):
    #url_connect is a Session object that allows you to persist
    url_connect = requests.Session()
    url_connect.headers['User-Agent'] = USER_AGENT          #User-Agent retrieves and presents Web content
    url_connect.headers['Accept-Language'] = LANGUAGE       #Accept-Language defines the language intended for the end-user
    url_connect.headers['Content-Language'] = LANGUAGE      #Content-Language defines the language to be used to pull the content
    weather_url = url_connect.get(weather_url)              #Gets the user-entered URL of Google weather at a particular location 

    #weather_html stores html-parsed google weather page 
    weather_html = bs(weather_url.text, "html.parser")  
    
    #seven_days stores the HTML id "wob_dp" 
    seven_days = weather_html.find("div", attrs={"id": "wob_dp"})

    seven_days_weather = []
    seven_days_weather_dict = {}
    
    #for each day in the seven_days_weather array, find the html tag related to the weather data for each day
    for day in seven_days.findAll("div", attrs={"class": "wob_df"}):    
        day_name = day.findAll("div")[0].attrs['aria-label']    #day_name returns each day
        day_weather = day.find("img").attrs["alt"]              #day_weather returns the forecast for day_name
        day_temp = day.findAll("span", {"class": "wob_t"})      #find high/low temperature class
        day_max = day_temp[0].text  #high-temp for day_name
        day_min = day_temp[2].text  #low-temp for day_name

        #append day_name, day_weather, day_temp, day_max, and day_min to seven_days_weather array 
        seven_days_weather.append({"name": day_name, "current_weather": day_weather, "max_temperature": day_max, "min_temperature": day_min})
        seven_days_weather_dict['seven_days'] = seven_days_weather  #convert seven_days_weather array to dict for printing
    
    #format and print weather data from seven_days_weather_dict{}
    for each_day in seven_days_weather_dict["seven_days"]:
        print("="*40, each_day["name"], "="*40)
        print("The weather forecast for", each_day["name"], "is", each_day["current_weather"])  
        print(f"The high is: {each_day['max_temperature']}°F")
        print(f"The low is: {each_day['min_temperature']}°F")
    
    #csv_title variable holds the title of the csv file using the location html id
    #.split(,)[0] removes the State and Zipcode from the html tag
    #.replaces whitespaces for city names that are more than one word long 
    csv_title = weather_html.find("div", attrs={"id": "wob_loc"}).text.split(',')[0].replace(" ", "")

    #define csv header using seven_days_weather keys 
    keys = seven_days_weather[0].keys()

    #Create a directory to store one-day data csv files 
    try:
        os.mkdir("./SevenDayData")
    except OSError as e:
        pass

    #Save and output a csv file with the seven-day weather data 
    csv_file = f"{csv_title}_sevenday_data.csv"
    with open("./SevenDayData/" + csv_file, "w") as file:
        csvwriter = csv.DictWriter(file, keys)
        csvwriter.writeheader()
        csvwriter.writerows(seven_days_weather)

    #Connect to weather database that contains the oneday table 
    conn = psycopg2.connect(database="weather", user="nirmal", password="password", host="127.0.0.1", port="5432")
    
    #create cursor object to interact with the weather database 
    curs = conn.cursor()

    #Open <location>_sevenday_data.csv, read from the file and save data to database
    with open("./SevenDayData/" + csv_file, 'r') as f:
        next(f)
        curs.copy_from(f, 'sevenday_data', sep=',')
    
    conn.commit()

    return ("\n" * 2)

if __name__ == "__main__":
    googlweather_url = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather+"   #googlweather_url stores google weather url
    location = input("Enter the name of the city and state whose weather you want to know: ")     #store user-input city name
    location_weather_url = googlweather_url+location    #location_weather_url concatenates location to googleweather_url

    print(oneday_weather_storer(location_weather_url))  #run oneday_weather_storer
    print(sevenday_weather_storer(location_weather_url))    #run sevenday_weather_storer
