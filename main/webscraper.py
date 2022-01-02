#webscraper.py is used to scrape the content of various websites 
#and store the data in the MySQL database

import requests
from bs4 import BeautifulSoup

weather_page = requests.get("https://forecast.weather.gov/MapClick.php?lat=38.96342&lon=-77.4447")
weather_page_content = BeautifulSoup(weather_page.content, 'html.parser')
seven_day_data = weather_page_content.find(id="seven-day-forecast")
forecast_data = seven_day_data.find_all(class_= "tombstone-container")
tonight_data = forecast_data[0]
period = tonight_data.find(class_= "period-name").get_text()
img = tonight_data.find("img")
long_description = img['title']
short_description = tonight_data.find(class_= "short-desc").get_text()
temperature = tonight_data.find(class_= "temp").get_text()

print(period)
print(long_description)
print(short_description)
print(temperature)