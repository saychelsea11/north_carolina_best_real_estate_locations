import pandas as pd
import numpy as np
import requests
import json
from bs4 import BeautifulSoup

def format_dates(df):
    #Converting string dates to Pandas datetime format and only keeping month and year
    df_dates = df.iloc[:,9:]
    df_dates.columns = pd.Series(df_dates.columns).apply(lambda x: pd.to_datetime(x).to_period('m'))
    df = df.iloc[:,:9]
    df = pd.concat([df,df_dates],axis=1)
    return df

def filter_variables(df,cols=['RegionName','City','State','CountyName','SizeRank',pd.to_datetime('2012-01').to_period('m'),pd.to_datetime('2017-06').to_period('m')]):
    #Filtering the dataset by the variables that are needed
    df = df[cols]
    return df
    
def filter_nyc(df):
    #Filtering the dataset to only keep instances where the City is New York
    df = df[df['City']=='New York']
    return df
    
def filter_city_state(df,city,state):
    #Filtering the dataset by specific city and state
    df = df[(df['City']==city) & (df['State']==state)]
    return df
    
def rename_cols(df,cols):
    #Renaming the columns to more readable names
    df.columns = cols
    return df
    
def convert_zip_str(df):
    #Converting the values for the 'ZipCode' variable to string
    df['ZipCode'] = list(map(str,df['ZipCode']))
    return df
    
def extract_durham_neighborhoods(url):
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
    
    return neighborhoods