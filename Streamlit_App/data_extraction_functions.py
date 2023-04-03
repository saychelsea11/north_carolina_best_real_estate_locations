import pandas as pd
import numpy as np
import geopy
from geopy.geocoders import Nominatim
import requests
import json
from bs4 import BeautifulSoup

def retrieve_neighborhood_coordinates(address='Abercromby, Durham, North Carolina'):
    #Extracting sample coordinates for a given location
    #address = 'Abercromby, Durham, North Carolina'

    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(address,timeout=10)
    latitude = location.latitude
    longitude = location.longitude
    #print('The geograpical coordinate of ',address,' are {}, {}.'.format(latitude, longitude))
    
    return longitude, latitude
    
def extract_durham_neighborhoods(url):
    try:
        response = requests.get(url)
        bs = BeautifulSoup(response.content,'lxml')
        #search = bs.find_all('li')

        #Extracting data in 'ul' tag which contains neighborhood names
        ul_list = bs.find_all('ul')

        data = []

        for item in ul_list: 
          if item.get('class'):
            if "blogroll" in item.get('class'):
              data = item
            else: 
              continue

        #Extracting individual neighborhoods and storing them in a list
        li_list = data.find_all('li')

        neighborhoods = []

        for item in li_list: 
          neighborhoods.append(item.find('a').text)
    except:
        neighborhoods = []
        print ("Error while retrieving neighborhoods","\n")
    
    return neighborhoods