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
    
def filter_data_timespan(df,cols=['RegionName','City','State','CountyName','SizeRank'],
                        start_date=pd.to_datetime('2012-01').to_period('m'),end_date=pd.to_datetime('2017-06').to_period('m')):
    cols.extend([start_date,end_date])
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
    
def filter_cities(df,col_name,cities=['Raleigh','Durham','Chapel Hill','Cary','Morrisville']):
    #Filtering dataset by cities
    df = df[df[col_name].isin(cities)]
    return df

def filter_states(df,col_name,states=['NC']):
    #Filtering dataset by states
    df = df[df[col_name].isin(states)]
    return df
    
def rename_cols(df,start_date,end_date):
    #Renaming the columns to more readable names
    df = df.rename(columns={"RegionName":"ZipCode","CountyName":"County",start_date:"StartPrice",end_date:"EndPrice"})
    return df
    
def convert_zip_str(df,col_name):
    #Converting the values for the 'ZipCode' variable to string
    df[col_name] = list(map(str,df[col_name]))
    return df
    
def filter_data_pipeline(df,city_col_name,state_col_name,cols=['RegionName','City','State','CountyName','SizeRank'],
                        start_date='2012-01',end_date='2017-06',
                        cities=['Raleigh','Durham','Chapel Hill','Cary','Morrisville'],states=['NC']):
    start_date = pd.to_datetime(start_date).to_period('m')
    end_date = pd.to_datetime(end_date).to_period('m')
    df = format_dates(df)
    df = filter_data_timespan(df,cols,start_date,end_date)
    if len(cities) > 0: 
        df = filter_cities(df,city_col_name,cities)
    else: 
        pass
    if len(states) > 0:
        df = filter_states(df,state_col_name,states)
    else: 
        pass
    df = rename_cols(df,start_date,end_date)
    
    return df
    
    
    
    