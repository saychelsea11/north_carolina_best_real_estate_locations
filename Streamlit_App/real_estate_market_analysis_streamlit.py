import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
import requests
import json
import streamlit as st

from bs4 import BeautifulSoup
import geopy
from geopy.geocoders import Nominatim
from math_functions import *
from wrangling_functions import *
from plotting_functions import *
from data_extraction_functions import *

path = r'C:\Users\sdas\Github_DS\north_carolina_best_real_estate_locations\Datasets\Zip_zhvi_bdrmcnt_2_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv'
df_zillow = pd.read_csv(path)

st.write("""
## U.S. Real Estate Market Analysis
""")

#User input for state
state_choice = st.selectbox('Select state', sorted(pd.Series(df_zillow['State'].unique()).dropna()))
df_zillow = df_zillow[df_zillow['State']==state_choice]

#User input for cities
city_choice = st.multiselect('Select cities', sorted(pd.Series(df_zillow['City'].unique()).dropna()))

#User input for aggregate metric
metric_choice = st.selectbox('Select price analysis metric', ['Mean','Median'])
metric_choice = metric_choice.lower()

#Cleaning and wrangling dataset
df_zillow = filter_data_pipeline(df_zillow,city_col_name="City",state_col_name="State",
                cols=['RegionName','City','State','CountyName','SizeRank'],
                start_date='2012-01',end_date='2022-12',
                cities=city_choice,
                states=[])
                
#Adding price metrics
df_zillow = add_price_metrics(df_zillow,10)

#Aggregate by city - price
data = agg_by_city(df_zillow,'EndPrice',metric_choice)
uni_barplot(data,metric_choice,'City','Price($)')

#Aggregate by county - price
data = agg_by_county(df_zillow,'EndPrice',metric_choice)
uni_barplot(data,metric_choice,'County','Price($)')

#Aggregate by city - price increase percentage
data = agg_by_city(df_zillow,'PriceIncreasePerc',metric_choice)
uni_barplot(data,metric_choice,'City','Price Increase (%)')

#Aggregate by county - price increase percentage
data = agg_by_county(df_zillow,'PriceIncreasePerc',metric_choice)
uni_barplot(data,metric_choice,'County','Price Increase (%)')

#Comparison by county - price increase percentage
uni_scatterplot(df_zillow,'PriceIncreasePerc','Housing price increase per year (%)')