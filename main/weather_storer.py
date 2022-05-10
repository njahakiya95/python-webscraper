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
from bs4 import BeautifulSoup as bs 
from requests.sessions import session

#USER_AGENT defines the acceptable browsers to scrape from and prevents our bot from being detected 
#LANGUAGE defines the language in which the scraping will be performed 
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
LANGUAGE = "en-US,en;q=0.5"

