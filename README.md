# Python Weather Scraper

weather-scraper.py takes a user input location (Lat/Lon Coordinates, City Name, Zip Code) 
and outputs the current time, temperature, humidity, wind, and chance of precipitation. 

If no input location is provided, the default location is the IP of the computer being used to run the code.

Furthermore, it also prints the 7 day forecast, along with the high/low temperature for each day. 

Google weather is used to perform the data scraping

To run the code, simple clone the repository and run the following command from your terminal ("location" is optional)
```
$ python3 weather-scraper.py "<location>"

```

**Example**
```
$ python3 weather-scraper.py "New York"

```

'''
Right now it is Sunday 8:00 PM in New York, NY
The weather is 41 °F and Partly cloudy
There is a  1% chance of precipitation
The humiditiy is 63% and the wind is 15 mph




The seven day forecast is:
======================================== Sunday ========================================
The weather forecast for Sunday is Mostly cloudy
The high is: 59°F
The low is: 30°F
======================================== Monday ========================================
The weather forecast for Monday is Snow showers
The high is: 33°F
The low is: 22°F
======================================== Tuesday ========================================
The weather forecast for Tuesday is Mostly sunny
The high is: 36°F
The low is: 30°F
======================================== Wednesday ========================================
The weather forecast for Wednesday is Showers
The high is: 45°F
The low is: 36°F
======================================== Thursday ========================================
The weather forecast for Thursday is Mostly cloudy
The high is: 39°F
The low is: 33°F
======================================== Friday ========================================
The weather forecast for Friday is Snow showers
The high is: 37°F
The low is: 23°F
======================================== Saturday ========================================
The weather forecast for Saturday is Mostly sunny
The high is: 35°F
The low is: 31°F
======================================== Sunday ========================================
The weather forecast for Sunday is Mostly cloudy
The high is: 43°F
The low is: 34°F
'''