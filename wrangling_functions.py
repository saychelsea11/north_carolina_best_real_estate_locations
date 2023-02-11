import pandas as pd
import numpy as np

def filter_variables(df):
    #Filtering the dataset by the variables that are needed
    df = df[['RegionName','City','State','CountyName','SizeRank','2012-01','2017-06']]
    return df
    
def filter_nyc(df):
    #Filtering the dataset to only keep instances where the City is New York
    df = df[df['City']=='New York']
    return df
    
def filter_city_state(df,city,state):
    #Filtering the dataset by specific city and state
    df = df[(df['City']==city) & (df['State']==state)]
    return df
    
def rename_cols(df):
    #Renaming the columns to more readable names
    df = df.rename(columns={'RegionName':'ZipCode','2012-01':'Price2012','2017-06':'Price2017','CountyName':'County'})
    return df
    
def convert_zip_str(df):
    #Converting the values for the 'ZipCode' variable to string
    df['ZipCode'] = list(map(str,df['ZipCode']))
    return df